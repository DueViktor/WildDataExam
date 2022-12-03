import pandas as pd
import matplotlib.pyplot as plt
import dtale
import numpy as np

threshold = 0.7


dataset_raw = pd.read_csv('data/final_datasets/aggregated_dataset.tsv',sep=';')
print(dataset_raw.sort_values('date').head())
dataset = dataset_raw[['date','High','Low','Mean','event_id','event_type','period_type']].drop_duplicates()


dims = ['conflict','similarity','knowledge','power','status','support','identity','romance','trust','fun']


corr_dfs = {}
for et in dataset['event_type'].unique():

    if isinstance(et,float):
        et = 'NoEvent'
        dataset_onehot = dataset_raw.loc[(dataset_raw['event_type'].isna())]
    else:
        dataset_onehot = dataset_raw.loc[(dataset_raw['event_type']==et)]
    print(dataset_onehot.shape)
    
    for dim in dims:
        dataset_onehot[dim] = dataset_onehot[dim].apply(lambda x:1  if x>threshold else 0)

    cols = ['date']+dims+['Mean']
    dataset_onehot = dataset_onehot[cols].groupby('date').sum().sort_index()
    dataset_out = dataset_onehot.rolling(6,center=True).mean().dropna().sort_index()
    for dim in dims:
        mu = dataset_out[dim].mean()
        std = dataset_out[dim].std()
        if std:
            dataset_out[dim] = dataset_out[dim].apply(lambda x: (x-mu)/std)
            
        else:
            dataset_out.drop(dim,axis=1,inplace=True)
            print('Dropping',dim)
    ## Z SCORE
    if et not in corr_dfs:
        corr_dfs[et] = dataset_out.sort_index()
    else:
        corr_dfs[et] = pd.concat([corr_dfs[et],dataset_out])
            


for k,v in corr_dfs.items():
    v.reset_index().to_csv('data/final_datasets/{}_zscores.csv'.format(k),index=None,sep=';')


