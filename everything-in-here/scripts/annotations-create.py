"""Analysis of how well we the annotations were done."""
from collections import defaultdict
from statsmodels.stats.inter_rater import fleiss_kappa, aggregate_raters
import os
import pandas as pd
from sklearn.metrics import cohen_kappa_score
import numpy as np
import json

# master json file for all the annotations
annotate = pd.read_csv("data/annotation-task/data.csv")

master = annotate.to_dict(orient="index")

for entry in master:
    try:
        master[entry]["text"] = master[entry]["text"].strip()
    except AttributeError:
        master[entry]["text"] = ""

    master[entry]["annotations"] = {}

# Change the key to be the "id" of the entry
master = {entry["id"]: entry for entry in master.values()}

# read in the files from annotation_path one by one and create a dataframe.
annotation_path = "data/annotation-task/individual-annotations/"
annotation_files = [
    file for file in os.listdir(annotation_path) if file.endswith(".json")
]

for file_path in annotation_files:
    
    name = file_path.replace(".json", "")
    
    print(os.path.join(annotation_path, file_path))
    
    file = json.load(open(os.path.join(annotation_path, file_path)))
    
    for entry in file:

        id_ = entry["data"]["id"]

        if id_ in master:

            try:
                choices = entry["annotations"][0]["result"][0]["value"]["choices"]
                master[id_]["annotations"][name] = choices

            except IndexError:
                
                if entry["annotations"][0]["result"] == []:
                    choices = []
                    master[id_]["annotations"][name] = []
                else:
                    raise IndexError
        else:
            print("Entry not in master", id_)
            continue

def create_annotation_grid(annotations):
    # Create a grid of annotations for each annotator
    
    assert isinstance(annotations, dict)

    all_annotations = set()
    for annotator in annotations:
        all_annotations.update(annotations[annotator])

    annotation_grid = pd.DataFrame(
        index=[annotator for annotator in annotations], columns=all_annotations
    )

    for annotator in annotations:
        for annotation in annotations[annotator]:
            annotation_grid.loc[annotator, annotation] = 1

    annotation_grid.fillna(0, inplace=True)

    return annotation_grid


# calculate the kappa score and fleiss kappa score for each annotator and entry

for entry in master:

    master[entry]["inter-annotation-agreement"] = defaultdict(dict)

    annotation_grid = create_annotation_grid(master[entry]["annotations"])

    # Calculate the inter-annotator agreement for each annotator

    for annotator_one in master[entry]["annotations"]:
        for annotator_two in master[entry]["annotations"]:

            if annotator_one != annotator_two:

                annotations_from_annotator_one = master[entry]["annotations"][
                    annotator_one
                ]
                annotations_from_annotator_two = master[entry]["annotations"][
                    annotator_two
                ]

                if sorted(annotations_from_annotator_one) == sorted(
                    annotations_from_annotator_two
                ):
                    master[entry]["inter-annotation-agreement"][annotator_one][
                        annotator_two
                    ] = 1

                else:
                    one_hotted_annotations_from_annotator_one = annotation_grid.loc[
                        annotator_one
                    ].values
                    one_hotted_annotations_from_annotator_two = annotation_grid.loc[
                        annotator_two
                    ].values

                    le_cohen = cohen_kappa_score(
                        one_hotted_annotations_from_annotator_one,
                        one_hotted_annotations_from_annotator_two,
                    )
                    master[entry]["inter-annotation-agreement"][annotator_one][
                        annotator_two
                    ] = le_cohen

    # Fleiss kappa score    

    if annotation_grid.columns.size == 0:
        master[entry]["fleiss_kappa_score"] = np.nan
        continue

    if annotation_grid.columns.size == 1:

        annotation_sum = annotation_grid.sum()[0]

        if annotation_sum == 0:
            master[entry]["fleiss_kappa_score"] = np.nan
        else:
            master[entry]["fleiss_kappa_score"] = (
                annotation_sum / annotation_grid.size
            )  # self made metric

        continue

    annotations_for_fleiss = aggregate_raters(annotation_grid, n_cat=None)[0]
    fleiss_kappa_score = fleiss_kappa(annotations_for_fleiss)

    # if fleiss_kappa_score is nan, then there is only one annotated label and the fleiss_kappa_score is 1
    if np.isnan(fleiss_kappa_score):
        fleiss_kappa_score = 1

    master[entry]["fleiss_kappa_score"] = fleiss_kappa_score

# save master to a json file named annotations.json
print("Saving to data/created-datasets/annotations.json")
with open("data/created-datasets/annotations.json", "w") as f:
    json.dump(master, f)
