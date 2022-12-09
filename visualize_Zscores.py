import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the z_score dataset
dataset = pd.read_csv("data/final_datasets/FINAL_zscores.tsv", sep=";")

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
    plt.figure(figsize=(20, 10))
    plt.style.use("fivethirtyeight")
    # Plot the conflict dimension
    plt.plot(
        dataset["date"], dataset[dim], linewidth=1.5, label=dim[0].upper() + dim[1:]
    )
    # Make the plot readable
    plt.xticks(rotation=90)
    # Make x-axis ticks every 20 days
    plt.xticks(np.arange(0, len(dataset["date"]), 20), size=15)

    # Visualize event id 1, 2 and 3 as x-span
    for event_id in [1, 2, 3]:
        # Get the min and max date for the event
        min_date = dataset[(dataset["event_id"] == event_id)]["date"].min()
        max_date = dataset[(dataset["event_id"] == event_id)]["date"].max()
        if event_id == 1:
            # Plot the x-span
            plt.axvspan(
                min_date, max_date, color="green", alpha=0.3, label="Positive events"
            )
        else:
            # Plot the x-span
            plt.axvspan(min_date, max_date, color="green", alpha=0.3)

    # Visualize event id 4, 5 and 6 as x-span
    for event_id in [4, 5, 6]:
        # Get the min and max date for the event
        min_date = dataset[(dataset["event_id"] == event_id)]["date"].min()
        max_date = dataset[(dataset["event_id"] == event_id)]["date"].max()

        if event_id == 4:
            # Plot the x-span
            plt.axvspan(
                min_date, max_date, color="red", alpha=0.25, label="Negative events"
            )
        else:
            # Plot the x-span
            plt.axvspan(min_date, max_date, color="red", alpha=0.25)

    # Make dim with big letter
    dim = dim[0].upper() + dim[1:]

    # Create title with dim and bigger font
    plt.title(dim + " Dimension", fontsize=30)

    # Create legend with positve and negative events
    plt.legend()

    # Make x and y axis labels
    plt.xlabel("Date", fontsize=20)
    plt.ylabel("Z-score", fontsize=20)

    # Save figure
    plt.savefig("viz/dimension_plots/z_score_" + dim + ".png")


# Plot dimensions
for dim in dataset.columns[1:-4]:
    plot_dim(dim)
