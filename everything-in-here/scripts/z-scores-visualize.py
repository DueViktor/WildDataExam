"""
This script plots the z-scores for each dimension and saves the plots to the 
viz/dimension_plots folder

The script is reading the z-scores from the data/created-datasets/zscores.tsv file 
which is created by the z-scores-create.py script
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the z_score dataset
dataset = pd.read_csv("../data/created-datasets/FINAL_zscores.tsv", sep=";")

# Function for plotting a dimension
def plot_dim(dim):
    """
    Function for plotting a dimension

    Parameters
    ----------
    dim : str
        The dimension to plot

    Returns
    -------
    Saves the plot to the viz/dimension_plots folder
    """
    # Initialize figure
    plt.figure(figsize=(20, 10))
    # Set style
    plt.style.use("fivethirtyeight")

    # Plot the dimension
    plt.plot(
        dataset["date"], dataset[dim], linewidth=1.5, label=dim[0].upper() + dim[1:]
    )

    # Plot the standard deviation as a shaded area
    min_val = dataset[dim] - dataset[dim + "_sd"]
    max_val = dataset[dim] + dataset[dim + "_sd"]
    plt.fill_between(dataset["date"], min_val, max_val, alpha=0.2)

    # Make the plot readable
    plt.xticks(rotation=90)
    # Make x-axis ticks every 20 days
    plt.xticks(np.arange(0, len(dataset["date"]), 20), size=15)
    # Make yaxis limits
    plt.ylim(-6, 4)

    # Visualize event id 1, 2 and 3 as x-span
    for event_id in [1, 2, 3]:
        # Get the min and max date for the event
        min_date = dataset[(dataset["event_id"] == event_id)]["date"].min()
        max_date = dataset[(dataset["event_id"] == event_id)]["date"].max()
        if event_id == 1:
            # Plot the x-span
            plt.axvspan(
                min_date, max_date, color="green", alpha=0.2, label="Positive events"
            )
        else:
            # Plot the x-span
            plt.axvspan(min_date, max_date, color="green", alpha=0.2)

    # Visualize event id 4, 5 and 6 as x-span
    for event_id in [4, 5, 6]:
        # Get the min and max date for the event
        min_date = dataset[(dataset["event_id"] == event_id)]["date"].min()
        max_date = dataset[(dataset["event_id"] == event_id)]["date"].max()

        if event_id == 4:
            # Plot the x-span
            plt.axvspan(
                min_date, max_date, color="red", alpha=0.2, label="Negative events"
            )
        else:
            # Plot the x-span
            plt.axvspan(min_date, max_date, color="red", alpha=0.2)

    # Create legend with positve and negative events
    plt.legend()

    # Make x and y axis labels
    plt.xlabel("Date", fontsize=20)
    plt.ylabel("Z-score", fontsize=20)

    # Add second y-axis for number of posts as bar chart
    plt.twinx()
    plt.bar(
        dataset["date"],
        dataset[dim + "_n_posts"],
        alpha=0.2,
        label="Number of posts",
        color="darkblue",
    )
    plt.ylabel("Number of posts", fontsize=20)
    # Make y-axis twice as big as the other
    plt.gca().set_ylim(bottom=0, top=dataset[dim + "_n_posts"].max() * 2)
    # Remove gridlines of second y-axis
    plt.grid(False)
    # Move ticks so they align with the other y-axis
    plt.gca().yaxis.set_ticks_position("right")

    # Create title with dim and bigger font with more distance to the x-axis
    plt.title(dim[0].upper() + dim[1:] + " Dimension", fontsize=30, pad=20)
    plt.tight_layout()
    # Save figure
    plt.savefig("viz/dimension_plots/z_score_" + dim + ".png")


# Plot dimensions
for dim in dataset.columns[1:11]:
    print("Plotting " + dim)
    plot_dim(dim)
