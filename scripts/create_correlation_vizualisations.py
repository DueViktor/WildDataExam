import pandas as pd
import os
import plotly.express as px
import matplotlib.pyplot as plt
from datetime import date, timedelta
import dtale
import seaborn as sns


viz_path = "../vizualisations/"


fpath = "../data/created-datasets/"
filename = "FINAL_zscores.tsv"
df = pd.read_csv(fpath + filename, sep="\t")
raw_data = pd.read_csv(fpath + "aggregated_dataset.csv", sep=";")


sorted_cols = (
    raw_data[raw_data.columns[4:14]].median().sort_values(ascending=False).index
)

plt.style.use("fivethirtyeight")

colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
fte = []
for color in colors:
    fte.append(color)

plt.figure(figsize=[16, 9])
plt.title("10-Dimensional Distributions")
flierprops = dict(
    marker="o", markerfacecolor="None", markersize=5, alpha=0.2, markeredgecolor=fte[4]
)

sns.boxplot(data=df, width=0.5, linewidth=0.5, color=fte[0], flierprops=flierprops)
plt.savefig(viz_path + "boxplot.png")


posts_days = raw_data[["date", "id"]]
posts_pr_day = posts_days.groupby("date").count().reset_index()
posts_pr_day["activity"] = posts_pr_day["id"]
posts_pr_day.drop("id", axis=1, inplace=True)


corr_dict = {"dimension": []}


for event_type in df.event_type.unique():
    activity_df = pd.merge(
        df.loc[df["event_type"] == event_type], posts_pr_day, on="date"
    )
    corr_dict[event_type] = []
    cur_corr = activity_df.corr()["Close"]
    if not corr_dict["dimension"]:
        corr_dict["dimension"] = list(df.columns)[1:10] + ["activity"]
    for d in corr_dict["dimension"]:
        corr_dict[event_type].append(cur_corr[d])


corr_df = pd.DataFrame(corr_dict).set_index("dimension")


plt.figure(figsize=[12, 12])
sns.heatmap(
    corr_df.drop("activity", axis=0).sort_values("negative"),
    annot=True,
    vmin=-1,
    vmax=1,
    cmap="coolwarm",
)
plt.savefig(viz_path + "zscore_price_correlation.png")
