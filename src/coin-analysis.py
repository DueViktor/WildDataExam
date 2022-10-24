from config import COINS_DIR, VIZ_DIR

import pandas as pd
import os
import plotly.express as px
import matplotlib.pyplot as plt

coin_files = [filename for filename in os.listdir(
    f'{COINS_DIR}') if filename.endswith('.csv')]
coins = dict()
for coin_file in coin_files:
    coin_name = coin_file.replace('.csv', '').split('-')[-1]

    df = pd.read_csv(f'{COINS_DIR}/{coin_file}', index_col=0)
    coins[coin_name] = df

# Basic for each coin
for coin_name, coin_df in coins.items():
    # all time
    fig = px.line(
        coin_df,
        x="Date",
        y="Close",
        title=f'Closing price for {coin_name}')
    fig.write_html(f'{VIZ_DIR}/{coin_name}-allTime.html')
    fig.write_image(f'{VIZ_DIR}/{coin_name}-allTime.png')
    plt.clf()

    # correlation matrix
    pd.plotting.scatter_matrix(coin_df, figsize=(10, 10))  # ,**{'title':})
    plt.suptitle(f'{coin_name} correlation matrix')
    plt.savefig(f'{VIZ_DIR}/{coin_name}-correlations.png')
    plt.clf()

    correlation_matrix = coin_df.corr(method='pearson')
    correlation_matrix.to_csv(f'{VIZ_DIR}/{coin_name}-correlations.csv')
