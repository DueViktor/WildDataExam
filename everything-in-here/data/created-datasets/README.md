# Created Datasets

These are the datasets that have been created by the scripts the `scripts` folder in the root of this repository.

Table of Contents:
- `raw.csv` : 10 model dimension annotations for all the posts along with author, bot detection and date
- `events.csv`: Hand labeled events from the closing price of the bitcoin market. 
- `annotation.csv` : This `.csv` contain the merge of individual annotations of 187 reddit posts regarding five cryptocurrencies.
- `thresholds.csv`: yo
- `z_scores.csv`: Aggregated data set with z-scores for each dimension for each day. The data set contains:   
  - 10 columns: with the z-scores for each dimension for each day. 
  - 10 columns: with the standard deviation for each dimension for each day. 
  - 10 columns: with the number of posts classified within a dimension for each day.
  - 3 columns: with the event type, event id and period type for each day.
  - 1 column: with the closing bitcoin price for each day.
