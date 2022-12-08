import pandas as pd
import matplotlib.pyplot as plt
import dtale
import numpy as np

# Set threshold for binarizing labels
dimensional_thresholds = {
    "conflict": 0.4307594341891152,
    "similarity": 0.25042258473959833,
    "knowledge": 0.7951832256864669,
    "power": 0.2077113337193926,
    "status": 0.3232280425727367,
    "support": 0.0542994892224669,
    "identity": 0.37557719512419263,
    "romance": 1,
    "trust": 0.17556890451442433,
    "fun": 0.41641424761878115,
}
num_days_rolling_average = 7

# Load in the aggregated dataset
dataset_raw = pd.read_csv("data/final_datasets/aggregated_dataset.tsv", sep=";")

# Select subset of columns
dataset = dataset_raw[
    ["date", "High", "Low", "Mean", "event_id", "event_type", "period_type"]
].drop_duplicates()

# Initialize dimensions
dims = [
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

# Initialize dictionary with eventtype dataframes
corr_dfs = {}

# Iterate over the eventtypes ('positive','negative')
for et in dataset["event_type"].unique():

    # Check if event is nan values - then assign NoEvent values
    if isinstance(et, float):
        et = "NoEvent"
        # Find posts where no event happened
        dataset_onehot = dataset_raw.loc[(dataset_raw["event_type"].isna())]
    else:
        # Else find posts on days that have the current eventtype
        dataset_onehot = dataset_raw.loc[(dataset_raw["event_type"] == et)]

    # Iterate over dimensions and binarize based on the threshold defined in the top (for Bence)
    for dim in dims:
        # Overwrites each dimension with a binary value
        dataset_onehot[dim] = dataset_onehot[dim].apply(
            lambda x: 1 if x > dimensional_thresholds[dim] else 0
        )

    # Group event posts by date (summed)
    # Basically assigns a count of posts containing a given dimension for each day
    cols = ["date"] + dims + ["Mean"]
    dataset_onehot = dataset_onehot[cols].groupby("date").mean().sort_index()

    # Apply rolling average, essentially, iterating over the days,
    # taking the average over the previous 3 days and 3 next days
    # and assigning this value
    # The first and last 3 days will be empty as they don't have enough preceding og succeeding days.
    #### These days are dropped
    dataset_out = (
        dataset_onehot.rolling(num_days_rolling_average, center=True)
        .mean()
        .dropna()
        .sort_index()
    )

    # Iterating over the dimensions, calculating the mean and std in order to calculate the z-score
    # z_score(x) = (x-mean(X))/std(X)
    for dim in dims:
        # Get mu
        mu = dataset_out[dim].mean()

        # Get std
        std = dataset_out[dim].std()

        # Check if any values over the threshold for a dimension - if not we would accidentally divide by zero
        # Only an issue for identity
        if std:
            # Calculate z-score and overwrite value for each dimension
            dataset_out[dim] = dataset_out[dim].apply(lambda x: (x - mu) / std)

        else:
            # Drop empty dimensions
            dataset_out.drop(dim, axis=1, inplace=True)
            print("Dropping", dim)

    # Save to dictionary - conditional may be obsolete
    if et not in corr_dfs:
        corr_dfs[et] = dataset_out.sort_index()
    else:
        corr_dfs[et] = pd.concat([corr_dfs[et], dataset_out])


# save the dataframes to the final_datasets directory
for k, v in corr_dfs.items():
    v.reset_index().to_csv(
        "data/final_datasets/{}_zscores.csv".format(k), index=None, sep=";"
    )
