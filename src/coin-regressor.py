"""
Idea: Is it neccesary to add more data to the coin features or would it be possible to estimate the prices without?
Could be the comparison and reasoning behind the reddit scrape.

I guess the data should be specified more towards the period we are looking add.

A lot from this one: https://www.geeksforgeeks.org/stock-price-prediction-using-machine-learning-in-python/
"""
from datetime import datetime
import os
from config import COINS_DIR, VIZ_DIR

import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn import metrics

coin_files = [filename for filename in os.listdir(
    f'{COINS_DIR}') if filename.endswith('.csv')]
coins = dict()
for coin_file in coin_files:
    coin_name = coin_file.replace('.csv', '').split('-')[-1]
    df = pd.read_csv(f'{COINS_DIR}/{coin_file}', index_col=0)
    coins[coin_name] = df

for coin_name, coin_df in coins.items():

    # don't use "with open" because of large indentation
    coin_prediction_file = open(f'{VIZ_DIR}/{coin_name}-predictions.txt', 'a+')
    sttime = datetime.now().strftime('%Y%m%d_%H:%M:%S - ')
    coin_prediction_file.write(f'## {sttime}\n')

    """ 0 if decrease and 1 if increase.
    If at day 0 the closing is 10 and at day 1 the closing is 20, the stock should have been bought.
    We're not interested in the precise price, but only whether or not the stock should be bought.
    Feature "buy" is a boolean indicator """
    coin_df['Buy'] = np.where(
        coin_df['Close'].shift(-1) > coin_df['Close'], 1, 0)

    # no date needed
    coin_df.drop('Date', inplace=True, axis='columns')

    # split to x and y
    X, y = coin_df.drop(labels=['Buy'], inplace=False,
                        axis='columns'), coin_df['Buy']

    # add a feature
    X['high-low'] = coin_df['High'] - df['Low']

    # write columns
    coin_prediction_file.write('cols: ' + ', '.join(X.columns.values) + '\n')

    # Predict
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.1, random_state=42)

    # scale it
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Tested models
    models = [LogisticRegression(), SVC(kernel='poly', probability=True)]

    for model in models:
        model.fit(X_train, y_train)
        # returns pred for both class 0 and 1. Output only 1
        train_pred = model.predict_proba(X_train)[:, 1]
        test_pred = model.predict_proba(X_test)[:, 1]

        coin_prediction_file.write(f'{type(model).__name__} : \n')
        coin_prediction_file.write(
            f'Training Accuracy : {metrics.roc_auc_score(y_train, train_pred):.3}\n')
        coin_prediction_file.write(
            f'Validation Accuracy : {metrics.roc_auc_score(y_test, test_pred):.3}\n\n')

    coin_prediction_file.close()
