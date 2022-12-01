"""
Analysis of how well we the annotations were done.

"""
from statsmodels.stats.inter_rater import fleiss_kappa,aggregate_raters
import time
import os
import pandas as pd
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import confusion_matrix
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import itertools
import json

# master json file for all the annotations
annotate = pd.read_csv("data/annotation/data.csv")

master = annotate.to_dict(orient='index')
for entry in master:
    try:
        master[entry]["text"] = master[entry]["text"].strip()
    except AttributeError:
        master[entry]["text"] = ""
    master[entry]['annotations'] = {}

# read in the files from annotation_path one by one and create a dataframe.
annotation_path = "data/annotation/annotated"
annotation_files = [file for file in os.listdir(annotation_path) if file.endswith(".json")]

for file_path in annotation_files:
    
    name = file_path.replace(".json", "")
    print(os.path.join(annotation_path, file_path))
    file = json.load(open(os.path.join(annotation_path, file_path)))

    for entry in file:

        if entry["id"] in master:
            try:
                choices =  entry["annotations"][0]["result"][0]["value"]["choices"]
                master[entry["id"]]["annotations"][name] = choices

            except IndexError:
                if entry["annotations"][0]["result"] == []:
                    choices = []
                    master[entry["id"]]["annotations"][name] = []
                else:
                    raise IndexError
        
        
### calculate the kappa score for each annotator
# how to calculate the kappa score for multiple annotators
# calculate the kappa score for each annotator
for entry in master:
    
    all_annotations = set()
    
    for annotation in master[entry]["annotations"]:
        for annotator in master[entry]["annotations"]:
            all_annotations.update(master[entry]["annotations"][annotator])

    number_of_annotators = len(master[entry]["annotations"])
    
    if number_of_annotators > 0:
        annotation_grid = pd.DataFrame(index=range(number_of_annotators), columns=all_annotations)
        
        for idx,annotator in enumerate(master[entry]["annotations"]):
            for annotation in master[entry]["annotations"][annotator]:
                annotation_grid.loc[idx, annotation] = 1
        
        annotation_grid.fillna(0, inplace=True)
        annotations_for_fleiss = aggregate_raters(annotation_grid, n_cat=None)[0]
        
        score = fleiss_kappa(annotations_for_fleiss)

        # if score is nan, then there is only one annotated label and the score is 1
        if np.isnan(score):
            score = 1
    
    else:
        score = 0

    master[entry]["fleiss-kappa"] = score
    

# save master to a json file named master.json
with open("data/annotation/master.json", "w") as f:
    json.dump(master, f)