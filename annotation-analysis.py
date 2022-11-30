"""
Analysis of how well we the annotations were done.

"""
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

# save master to a json file named master.json
with open("data/annotation/master.json", "w") as f:
    json.dump(master, f)