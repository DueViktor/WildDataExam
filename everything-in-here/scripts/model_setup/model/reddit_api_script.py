import pandas as pd
import numpy as np

import json
import time
import datetime as dt
import os
from pmaw import PushshiftAPI

api = PushshiftAPI(num_workers=os.cpu_count() * 3)

start_time = time.time()
sub_reddits = ["bitcoin", "ethereum", "xrp", "solana", "polkadot"]


all_months = {
    1: 31,
    2: 28,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31,
}


def save_submissions(after, before, limit, subreddits):
    submissions = api.search_submissions(
        subreddit=subreddits[0], before=before, after=after, limit=limit
    )
    sub_df = pd.DataFrame(submissions)
    try:
        print(sub_df.iloc[0])
    except:
        print("failed")
        return
    for subreddit in sub_reddits[1:]:
        submissions = api.search_submissions(
            subreddit=subreddit, before=before, after=after, limit=limit
        )
        new_df = pd.DataFrame(submissions)
        sub_df = sub_df.append(new_df)
    sub_df["concated"] = sub_df["title"] + "\n" + sub_df["selftext"]
    date_str = dt.datetime.utcfromtimestamp(before).strftime("%Y_%m_%d")
    sub_df.to_csv(
        f"reddit-dataset/submissions_{date_str}_reddit.tsv", sep="\t", index=False
    )
    print(date_str, "_sub_done")
    comments = api.search_comments(
        subreddit=subreddits[0], before=before, after=after, limit=limit
    )
    com_df = pd.DataFrame(comments)
    for subreddit in sub_reddits[1:]:
        comments = api.search_comments(
            subreddit=subreddit, before=before, after=after, limit=limit
        )
        new_df = pd.DataFrame(comments)
        com_df = com_df.append(new_df)
    com_df.to_csv(
        f"reddit-dataset/comments_{date_str}_reddit.tsv", sep="\t", index=False
    )


for month, month_length in all_months.items():
    for i in range(1, month_length):

        before = int(dt.datetime(2022, month, i + 1, 0, 0, 0).timestamp())
        after = int(dt.datetime(2022, month, i, 0, 1, 0).timestamp())
        limit = 200
        print("starting")
        save_submissions(after, before, limit, sub_reddits)
    before = int(dt.datetime(2022, month + 1, 1, 0, 0, 0).timestamp())
    after = int(dt.datetime(2022, month, month_length, 0, 0, 0).timestamp())
    save_submissions(after, before, limit, sub_reddits)

    print("Finished at {}".format(str(time.time())))
