from config import COINS_DIR, VIZ_DIR

import pandas as pd
import os
import plotly.express as px


coin_files = [filename for filename in os.listdir(COINS_DIR) if filename.endswith('.csv')]

for coin_file in coin_files:
    coin_name = coin_file.replace('.csv','').split('-')[-1]
    df = pd.read_csv(f'{COINS_DIR}/{coin_file}',index_col=0)

    # ALL TIME
    fig = px.line(df, x="Date", y="Close", title=f'Closing price for {coin_name}')
    fig.write_html(f'{VIZ_DIR}/{coin_name}.html')
    fig.write_image(f'{VIZ_DIR}/{coin_name}.png')
