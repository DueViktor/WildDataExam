"""
Visualize the three events from notion
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


btc = pd.read_csv("data/coins/coinmarket-BTC.csv", index_col=0)[['Date','Close']]

btc = btc[btc["Date"] >= "2022-01-01"]
# apply rolling mean to Close from 7 before to 7 after
btc["RollingClose"] = btc["Close"].rolling(14,min_periods=1).mean()
# plot the rolling mean and the close using plotly
fig = px.line(btc, x="Date", y=["Close", "RollingClose"], title="BTC Close and Rolling Close")

# 1. 
fig.add_vrect(x0="2022-03-05", x1="2022-04-04", fillcolor="blue", opacity=0.25, line_width=0)
fig.add_vline(x="2022-03-13", line_width=1, line_dash="dash", line_color="black")
fig.add_vline(x="2022-03-29", line_width=1, line_dash="dash", line_color="black")

# 2.
fig.add_vrect(x0="2022-01-27", x1="2022-02-16", fillcolor="blue", opacity=0.25, line_width=0)
fig.add_vline(x="2022-02-03", line_width=1, line_dash="dash", line_color="black")
fig.add_vline(x="2022-02-09 ", line_width=1, line_dash="dash", line_color="black")

# 3.
fig.add_vrect(x0="2022-02-23", x1="2022-03-07", fillcolor="blue", opacity=0.25, line_width=0)
fig.add_vline(x="2022-02-03", line_width=1, line_dash="dash", line_color="black")
fig.add_vline(x="2022-03-01", line_width=1, line_dash="dash", line_color="black")

# Negative events
# 4.
fig.add_vrect(x0="2022-06-01", x1="2022-07-01", fillcolor="red", opacity=0.25, line_width=0)
fig.add_vline(x="2022-06-07", line_width=1, line_dash="dash", line_color="black")
fig.add_vline(x="2022-06-18", line_width=1, line_dash="dash", line_color="black")
# 5.
fig.add_vrect(x0="2022-04-27", x1="2022-05-19", fillcolor="red", opacity=0.25, line_width=0)
fig.add_vline(x="2022-05-04", line_width=1, line_dash="dash", line_color="black")
fig.add_vline(x="2022-05-12", line_width=1, line_dash="dash", line_color="black")
# 6.
fig.add_vrect(x0="2022-01-12", x1="2022-01-30", fillcolor="red", opacity=0.25, line_width=0)
fig.add_vline(x="2022-01-18", line_width=1, line_dash="dash", line_color="black")
fig.add_vline(x="2022-01-22", line_width=1, line_dash="dash", line_color="black")

# fig.show()
fig.write_html("viz/BTC-with-events.html")
fig.write_image("viz/BTC-with-events.png")