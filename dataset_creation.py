import pandas as pd
import os
import random
from tqdm import tqdm


def load_data():
    filepath = "data/labelled_data/"
    all_files = os.listdir(filepath)
    comments = {}
    posts = {}
    for fname in tqdm(all_files):
        file = pd.read_csv(filepath + fname, sep="\t").drop("Unnamed: 0", axis=1)
        if "submission" in fname:
            posts["_".join(fname.split("_")[3:6])] = file
        if "comment" in fname:
            comments["_".join(fname.split("_")[3:6])] = file

    subset = []
    for date, df in posts.items():
        df["date"] = date
        df["text_type"] = "post"
        subset.append(df)

    merged_posts = pd.concat(subset)
    subset = []
    for date, df in comments.items():
        df["date"] = date
        df["text_type"] = "comment"
        subset.append(df)

    merged_comments = pd.concat(subset)

    cols = [
        "id",
        "author",
        "corpus",
        "date",
        "text_type",
        "subreddit",
        "conflict",
        "similarity",
        "knowledge",
        "power",
        "status",
        "support",
        "identity",
        "romance",
        "trust",
        "fun",
    ]
    posts_df = merged_posts[cols]
    comments_df = merged_comments[cols]

    return posts_df, comments_df


def load_BTC_data():
    coin_path = "data/coins/"
    coin_fnames = os.listdir(coin_path)
    coin_frames = {
        fname.split(".")[0]
        .split("-")[1]: pd.read_csv(coin_path + fname)
        .drop("Unnamed: 0", axis=1)
        for fname in coin_fnames
    }

    BTC_prices = coin_frames["BTC"]
    BTC_prices["Date"] = BTC_prices["Date"].apply(lambda x: x.replace("_", "-"))
    return BTC_prices


def aggregate_comments(posts_df, comments_df):
    sources = ["posts", "comments", "combined"]
    source_map = {
        "posts": posts_df,
        "comments": comments_df,
        "combined": pd.concat([posts_df, comments_df]),
    }

    source_choice = sources[-1]

    cols = [
        "id",
        "author",
        "corpus",
        "date",
        "conflict",
        "similarity",
        "knowledge",
        "power",
        "status",
        "support",
        "identity",
        "romance",
        "trust",
        "fun",
    ]

    source_df = source_map[source_choice]

    btc_reddit = source_df.loc[source_df.subreddit == "Bitcoin"][cols].sort_values(
        "date"
    )
    btc_reddit["date"] = btc_reddit["date"].apply(lambda x: x.replace("_", "-"))
    return btc_reddit


def merge(btc_reddit, BTC_prices):

    btc_full = pd.merge(
        btc_reddit,
        BTC_prices[["Date", "High", "Low", "Close"]],
        left_on="date",
        right_on="Date",
    ).drop("Date", axis=1)

    return btc_full


def create_btc_full():
    posts_df, comments_df = load_data()
    BTC_prices = load_BTC_data()
    btc_reddit = aggregate_comments(posts_df, comments_df)
    btc_full = merge(btc_reddit, BTC_prices)

    return btc_full


def create_event_frame():
    event_dict = {
        "eventID": [1, 2, 3, 4, 5, 6],
        "before_start": [
            "2022-03-05",
            "2022-01-27",
            "2022-02-23",
            "2022-06-01",
            "2022-04-27",
            "2022-01-12",
        ],
        "before_end": [
            "2022-03-13",
            "2022-02-03",
            "2022-02-27",
            "2022-06-07",
            "2022-05-04",
            "2022-01-18",
        ],
        "during_start": [
            "2022-03-13",
            "2022-02-03",
            "2022-02-27",
            "2022-06-07",
            "2022-05-04",
            "2022-01-18",
        ],
        "during_end": [
            "2022-03-28",
            "2022-02-09",
            "2022-03-01",
            "2022-06-18",
            "2022-05-12",
            "2022-01-22",
        ],
        "after_start": [
            "2022-03-28",
            "2022-02-09",
            "2022-03-01",
            "2022-06-18",
            "2022-05-12",
            "2022-01-22",
        ],
        "after_end": [
            "2022-04-04",
            "2022-02-16",
            "2022-03-07",
            "2022-07-01",
            "2022-05-19",
            "2022-01-30",
        ],
        "event_type": [
            "positive",
            "positive",
            "positive",
            "negative",
            "negative",
            "negative",
        ],
    }

    event_frame = pd.DataFrame(event_dict)
    return event_frame


def assign_events(event_frame, btc_full):

    periods = []

    for k, row in tqdm(event_frame.iterrows()):
        before = btc_full.loc[
            (btc_full["date"] > row["before_start"])
            & (btc_full["date"] <= row["before_end"])
        ]
        if before.shape[0]:
            before["event_id"] = [row["eventID"]] * before.shape[0]
            before["event_type"] = [row["event_type"]] * before.shape[0]
            before["period_type"] = ["before"] * before.shape[0]
            periods.append(before)

        during = btc_full.loc[
            (btc_full["date"] > row["during_start"])
            & (btc_full["date"] <= row["during_end"])
        ]
        if during.shape[0]:
            during["event_id"] = [row["eventID"]] * during.shape[0]
            during["event_type"] = [row["event_type"]] * during.shape[0]
            during["period_type"] = ["during"] * during.shape[0]
            periods.append(during)

        after = btc_full.loc[
            (btc_full["date"] > row["after_start"])
            & (btc_full["date"] <= row["after_end"])
        ]
        if after.shape[0]:
            after["event_id"] = [row["eventID"]] * after.shape[0]
            after["event_type"] = [row["event_type"]] * after.shape[0]
            after["period_type"] = ["after"] * after.shape[0]
            periods.append(after)

    df_temp = pd.concat(periods)

    boring = btc_full.loc[~btc_full.date.isin(df_temp.date.values)]
    boring["period_type"] = [None] * boring.shape[0]
    boring["event_id"] = [None] * boring.shape[0]
    boring["event_type"] = [None] * boring.shape[0]
    final = pd.concat([df_temp, boring])

    final.to_csv("data/final_datasets/aggregated_dataset.csv", index=None, sep=";")


if __name__ == "__main__":
    event_frame = create_event_frame()
    btc_full = create_btc_full()
    assign_events(event_frame, btc_full)
