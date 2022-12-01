import pandas as pd
import matplotlib.pyplot as plt
import dtale
import numpy as np

threshold = 0.8




dataset_raw = pd.read_csv('data/final_datasets/aggregated_dataset.tsv',sep=';')
dataset = dataset_raw[['date','High','Low','Mean','event_id','event_type','period_type']].drop_duplicates()





dims = ['conflict','similarity','knowledge','power','status','support','identity','romance','trust','fun']


corr_dfs = {}
for et in dataset['event_type'].unique():
    if isinstance(et,float):
        continue
    
    dataset_onehot = dataset_raw.loc[(dataset_raw['event_type']==et)]

    for dim in dims:
        dataset_onehot[dim] = dataset_onehot[dim].apply(lambda x:1  if x>threshold else 0)


    cols = ['date']+dims

    ## Z SCORE

    if et not in corr_dfs:
        corr_dfs[et] = dataset_onehot[cols]
    else:
        corr_dfs[et] = pd.concat([corr_dfs[et],dataset_onehot[cols]])
            


print(corr_dfs['positive'].shape)
print(corr_dfs['negative'].shape)
print(corr_dfs['positive'].head())
