import json
import pandas as pd
from statistics import mean, median
from collections import Counter
from tqdm import tqdm
import os
# need to find new path for the needed files

def load_data(path='../data/raw/train.json'):

    with open(path,'r') as file:
        data = json.load(file)

    return data
#loading annotation dataset
ann_data = load_data(path = '../data/created-datasets/annotations.json' )

#Loading all the reddit posts that we've downloaded 
filepath = "../data/raw_data/labelled_data/"
all_files = os.listdir(filepath)
comments = {}
posts = {}
for fname in tqdm(all_files):
    file = pd.read_csv(filepath+fname,sep='\t').drop('Unnamed: 0',axis=1)
    if 'submission' in fname:
        posts['_'.join(fname.split('_')[3:6])] = file
subset = []
for date,df in posts.items():
    df['date'] = date
    subset.append(df)


# All reddit posts DataFrame with the 10 dimention scores
merged_posts = pd.concat(subset)



dims = ['conflict','similarity','knowledge','power','status','support','identity','romance','trust','fun']
scores_per_dim = { dim : [] for dim in dims}
cnt = 0
ids_not_fount= []
for idx, dp in ann_data.items():

    row_df = merged_posts.loc[merged_posts['id'] == dp['id']]
    if row_df.shape[0] == 1:
        temp_dim_cnt = Counter()
        annotator_cnt = len(dp['annotations'])
        for annotator, labels in dp['annotations'].items():
            
            labels =  [lab.lower() for lab in labels]
            temp_dim_cnt.update(labels) 
        
        for dim in dims:
            ann_ratio = 0
            if annotator_cnt != 0:
                ann_ratio = temp_dim_cnt[dim]/annotator_cnt
            
            scores_per_dim[dim].append((row_df[dim].iloc[0], ann_ratio))
    else:
        ids_not_fount.append(dp['id'])

# scores_per_dim is the main out put of the piece of code above
# scores_per_dim is a dictionary of list of tuples for each social dimension
# the first element of the tuple is the 10dim model score of the n_th post in the annotation dataset
# the second element is the fraction of annotators that annotated the n_th post to be in the social dimension


# In this section we calculate the fraction of annotations in each dimensions that we annotated to be in the given social dimnsion
dim_percentiles = {}
for dim in dims:
    
    ann_rs = list(zip(*scores_per_dim[dim]))[1]
    dim_percentiles[dim] = mean(ann_rs)

# dim_percentiles show the ratio of annotations that tells it appears in a post
# In this case it is the following:
'''
{'conflict': 0.026737967914438502,
 'similarity': 0.0481283422459893,
 'knowledge': 0.7363636363636363,
 'power': 0.03235294117647059,
 'status': 0.04090909090909091,
 'support': 0.09411764705882353,
 'identity': 0.04866310160427808,
 'romance': 0.00267379679144385,
 'trust': 0.15962566844919787,
 'fun': 0.055347593582887704}
'''

# In this section we pick a threshold by picking the top n top percent of the merged_posts
# of the given dimension for example for conflict the top 2.7 % and the lowest of these would be the 
# threshold

threshold_merged_posts = {}
for dim in dims:
    threshold_merged_posts[dim] = merged_posts[dim].quantile(1 - dim_percentiles[dim])


# save it into files
with open('../data/created-datasets/thresholds.json','w') as f:
    json.dump(threshold_merged_posts,f)