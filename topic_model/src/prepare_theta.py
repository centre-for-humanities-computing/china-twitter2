''' VMP 2022-03-05: 
based on Analysis_RASMUS.ipynb
'''

#### Imports
import pandas as pd 
import pickle as pkl 
import altair as alt
import numpy as np 
import os 
import re
import pyLDAvis
import gensim
import openpyxl
from pathlib import Path



def prep_data(filepath):
    """Preparing the data

    Returns:
        pd.Dataframes: Returns three dataframes - the whole dataset, the diplomats and the media.
    """    
    en_df = pd.read_csv(filepath)

    en_df['month'] = pd.DatetimeIndex(en_df['created_at']).month
    en_df['date'] = pd.DatetimeIndex(en_df['created_at']).date
    
    def retweet_binary(string):
        if string == "retweeted":
            return "Retweet"
        else:
            return "Other"

    en_df["retweet_bin"] = en_df["retweet"].apply(lambda x: retweet_binary(x))
    
    en_df["date"] = pd.to_datetime(en_df["date"])
    
    return en_df, en_df[en_df["category"] == "Diplomat"].reset_index(drop=True), en_df[en_df["category"] == "Media"].reset_index(drop=True)

def load_models(filepath_media, filepath_diplomat):
    with open(filepath_media, "rb") as f:
        media = pkl.load(f)
    
    with open(filepath_diplomat, "rb") as f:
        diplo = pkl.load(f)
        
    return media, diplo

def main():
    path = Path(__file__)

    mdl_path = path.parents[1] / 'theta'
    theta_path = path.parents[1] / 'fig'
    data_path = path.parents[2] / 'data'

    # load model
    for period in ["early", "late", "all"]:
        media_dict, diplo_dict = load_models(mdl_path / f'{period}dataMedia.pkl', mdl_path / f'{period}dataDiplomat.pkl')
        
        data, diplomats, media = prep_data(data_path / f"{period}_data_topic_model.csv")

        # diplomats without retweets
        diplo_without = diplomats[diplomats["retweet"] != "retweeted"].reset_index(drop = True)
        
        # Task 1: Diplomat document representation and metadata
        ## add $\theta$ to to diplomats

        ## comment0: diplo_without, model is trained without retweet to avoid redundancy
        ## comment1: corpus is filtered for extremes with Gensim 
        ## comment2 (VMP 2022-03-05): using max_topics, rather than len(theta[0]). 

        # predict theta_i on document in corpus 
        print(f'\n[INFO] predicting \u03B8...\n{"*"*25}')
        verbose = 5000
        theta = list()
        for i, doc in enumerate(diplo_dict['corpus']):
            vector = diplo_dict['model'][doc]
            theta.append(vector[0])
            if verbose > 0 and i > 0 and (i + 1) % verbose == 0:
                print(f'[INFO] processed {i + 1}/{len(diplo_dict["corpus"])}')
        # dimension consistent theta array
        ntopics_lst = [len(doc) for doc in theta]
        max_topics = max(ntopics_lst)
        print(f"maximum number of topics: {max_topics}")
        (m, k) = (len(theta), max_topics) #kappa VMP2022-03-05: (previously: (len(theta), len(theta[0])))
        theta_transform = np.zeros((m, k))
        for (i, doc) in enumerate(theta):
            theta_i = np.zeros((1,30)) # VMP: where is this used?
            for j, var in doc:
                theta_transform[i,j] = var
        # write to csv
        df = pd.DataFrame()
        for i in range(len(theta_transform[0,:])):
            df[f'var {i}'] = theta_transform[:,i]
        dfout = pd.concat([diplo_without, df], axis=1)
        fname = str(theta_path / f'diplomats_noretweet_theta_df_{period}.csv')
        dfout.to_csv(fname, index=False)
        print(f'{"*"*25}\n[INFO] data exported to {fname}')
        fname_maxqda = '..' + fname.split('.')[2] + '.xlsx' # VMP2022-03-05: (previously: fname.split('.')[0] + '.xlsx')
        dfout['created_at'] = dfout['created_at'].astype(str)
        dfout.to_excel(fname_maxqda, index=False)
        print(f'[INFO] data exported to {fname_maxqda}')