import pandas as pd
import matplotlib.pyplot as plt
import dtale
import numpy as np

# Import threshold data from data/annotation/thresholds.json
thresholds = pd.read_json("data/annotation/new_thresholds.json", orient="index")
# Rename column as threshold
thresholds = thresholds.rename(columns={0: "threshold"})

# Rolling average window size
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
    # Index threshold from thresholds dataframe
    threshold = thresholds.loc[dim]["threshold"]
    # Overwrites each dimension with a binary value
    dataset_raw[dim] = dataset_raw[dim].apply(lambda x: 1 if x > threshold else 0)

# Count number of scores above threshold for each day for each dimension
posts_per_day = dataset_raw.groupby(["date"]).sum()
# Remove columns that are not dimensions
posts_per_day = posts_per_day.drop(
    ["High", "Low", "Mean", "event_id", "romance"], axis=1
)

# Group event posts by date (summed)
# Basically assigns a count of posts containing a given dimension for each day
cols = ["date"] + dims
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
    # Get mu and std for each dimension
    mu = dataset_out[dim].mean()
    std = dataset_out[dim].std()
    # Get mu and std for standard deviation dataframe
    mu_sd = dataset_out_sd[dim].mean()
    std_sd = dataset_out_sd[dim].std()

    # Check if any values over the threshold for a dimension - if not we would accidentally divide by zero
    # Only an issue for identity
    if std:
        # Calculate z-score and overwrite value for each dimension
        dataset_out[dim] = dataset_out[dim].apply(lambda x: (x - mu) / std)
        # Calculate z-score for standard deviation dataframe
        dataset_out_sd[dim] = dataset_out_sd[dim].apply(lambda x: (x - mu_sd) / std_sd)

    else:
        # Drop empty dimensions
        dataset_out.drop(dim, axis=1, inplace=True)
        dataset_out_sd.drop(dim, axis=1, inplace=True)
        print("Dropping", dim)

# Merge with standard deviation dataframe
dataset_out = dataset_out.merge(
    dataset_out_sd, on="date", suffixes=("", "_sd"), how="left"
)

# Merge with posts per day dataframe
dataset_out = dataset_out.merge(
    posts_per_day, on="date", suffixes=("", "_n_posts"), how="left"
)

# Merge with event data
dataset_out = dataset_out.merge(events, on="date", how="left")

# Save the dataset
dataset_out.to_csv("data/final_datasets/FINAL_zscores.tsv", sep=";", index=None)
