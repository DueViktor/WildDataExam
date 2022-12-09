import pandas as pd
import numpy as np
import requests
import json
import time
import datetime as dt
import os
from pmaw import PushshiftAPI

api = PushshiftAPI(num_workers=os.cpu_count()*5)

subreddit = 'bitcoin'
before = int(dt.datetime(2022,8,1,0,0,0).timestamp())
after = int(dt.datetime(2022,3,1,0,0,0).timestamp())
limit = 10

submissions = api.search_submissions(subreddit=subreddit, before=before, after=after, limit=limit)
sub_df = pd.DataFrame(submissions)

#safe sub_df to csv
sub_df.to_csv('reddit-dataset/submission_trial.csv', index=False)