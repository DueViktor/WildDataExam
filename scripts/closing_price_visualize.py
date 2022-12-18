import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the z_score dataset
dataset = pd.read_csv("data/created-datasets/aggregated_dataset.csv", sep=";")

# Remove any duplicates in date column
dataset = dataset.drop_duplicates(subset="date")
# Sort the dataset by date
dataset = dataset.sort_values(by="date")

# Plot the closing price against the date
# Initialize figure
plt.figure(figsize=(20, 10))
# Set style
plt.style.use("fivethirtyeight")

# Plot the dimension
plt.plot(dataset["date"], dataset["Close"], linewidth=1.5, label="Closing price")

# Make the plot readable
plt.xticks(rotation=90)
# Make x-axis ticks every 20 days
plt.xticks(np.arange(0, len(dataset["date"]), 20), size=15)
# Make yaxis limits
# plt.ylim(-6, 4)

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
        plt.axvspan(min_date, max_date, color="red", alpha=0.2, label="Negative events")
    else:
        # Plot the x-span
        plt.axvspan(min_date, max_date, color="red", alpha=0.2)

# Create legend with positve and negative events
plt.legend()

# Make x and y axis labels
plt.xlabel("Date", fontsize=20)
plt.ylabel("Closing Price (USD)", fontsize=20)

# Create title
plt.title("Bitcoin closing price against time", fontsize=30)
plt.tight_layout()

# Save the figure
plt.savefig("visualisations/closing_price_with_events.png")
