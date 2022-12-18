import pandas as pd
import os
from tqdm import tqdm
import re

fpath = "../data/labelled_reddit_data/"
files = os.listdir(fpath)
files = [i for i in files if "2022_03" and ".tsv" in i]


dfs = {}
cc = 0
failed_files = []
for file in tqdm(files):
    try:
        data = pd.read_csv(fpath + file, sep="\t")
        dfs[file.replace(".tsv", "")] = data
        print(file)
        print(data.shape)
        print("\n\n\n")
    except:
        cc += 1
        failed_files.append(file)


def concat_cols(row):
    if row["title"] and row["selftext"]:
        return str(row["title"]) + " " + str(row["selftext"])

    elif row["title"]:
        return row["title"]

    elif row["selftext"]:
        return row["selftext"]


def create_corpus_column(fname, df):
    if "submission" in fname:
        df["corpus"] = [concat_cols(row) for k, row in df.iterrows()]
        return df

    elif "comment" in fname:
        df["corpus"] = df["body"]
        return df


def text_clean(
    text,
    stopwords=[
        "https",
        "com",
        "tr",
        "www",
        "ng",
        "nh",
        "th",
        "ch",
        "ti",
        "amp",
        "kh",
        "removed",
        "http",
    ],
):

    if text is None or isinstance(text, float):
        return ""

    text = text.lower()

    text = re.sub("[^0-9a-zA-Z]+", " ", text)
    for sw in stopwords:
        text = text.replace(sw, "")

    return text


def clean_corpus(df):
    df["corpus"] = df["corpus"].apply(lambda x: text_clean(x))
    return df


if __name__ == "__main__":

    for k, r in dfs.items():
        d = create_corpus_column(k, r)
        d = clean_corpus(d)
        d.to_csv(
            "model_setup/tendimensions/processed_data/cleaned_{}.tsv".format(k),
            sep="\t",
        )
