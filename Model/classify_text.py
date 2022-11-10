import tendims
import pandas as pd
import os
from tqdm import tqdm

def load_model():
    model = tendims.TenDimensionsClassifier(is_cuda=True, models_dir = './models/lstm_trained_models', 
                                            embeddings_dir='./embeddings')
    return model


def load_data(filepath):
    data = pd.read_csv(filepath,sep='\t')
    return data


def label_data(data,model,column='corpus'):
    dimensions = model.dimensions_list
    cur_corpus = data[column].values.tolist()
    for dim in dimensions:
        print('CLASSIFYING',dim.upper())
        cur_dim = []
        
        for sent in tqdm(cur_corpus):

            cur_dim.append(model.compute_score(sent, dim))

        data[dim] = cur_dim
    return data



def run_model(filepath=None,column = 'corpus',outpath = 'output/data/labeled_data.csv'):
    model = load_model()
    if not filepath:
        filepath = input('Input path to data')

    data  = load_data(filepath)

    data = label_data(data,model,column=column)


    print('Saving Data to',outpath)
    data.to_csv(outpath,index=None,sep='\t')


if __name__ == '__main__':
    for file in os.listdir('processed_data/'):
        run_model(filepath='processed_data/'+file,outpath = 'output/data/reddit/labeled_'+file)
