import pandas as pd
import matplotlib.pyplot as plt
import dtale
import numpy as np

# Set threshold for binarizing labels
threshold = 0.7
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

# Saving all event encordings
events = (
    dataset_raw[["date", "event_type", "period_type", "event_id"]]
    .drop_duplicates(subset=["date"], keep="first")
    .fillna(0)  # All non-event days are filled with 0
)

# Make event_id into integer
events["event_id"] = events["event_id"].astype(int)

# Iterate over dimensions and binarize based on the threshold defined in the top (for Bence)
for dim in dims:
    # Overwrites each dimension with a binary value
    dataset_raw[dim] = dataset_raw[dim].apply(lambda x: 1 if x > threshold else 0)

# Group event posts by date (summed)
# Basically assigns a count of posts containing a given dimension for each day
cols = ["date"] + dims + ["Mean"]
dataset_raw = dataset_raw[cols].groupby("date").mean().sort_index()

# Apply rolling average, essentially, iterating over the days,
# taking the average over the previous 3 days and 3 next days
# and assigning this value
# The first and last 3 days will be empty as they don't have enough preceding og succeeding days.
#### These days are dropped
dataset_out = (
    dataset_raw.rolling(num_days_rolling_average, center=True)
    .mean()
    .dropna()
    .sort_index()
)

# Create standard deviation dataframe for each dimension
dataset_out_sd = (
    dataset_raw.rolling(num_days_rolling_average, center=True)
    .std()
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

# Merge with standard deviation dataframe
dataset_out = dataset_out.merge(
    dataset_out_sd, on="date", suffixes=("", "_sd"), how="left"
)

# Merge with event data
dataset_out = dataset_out.merge(events, on="date", how="left")

# Save the dataset
dataset_out.to_csv("data/final_datasets/FINAL_zscores.tsv", sep=";", index=None)
