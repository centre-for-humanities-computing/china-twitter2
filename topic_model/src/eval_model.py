'''
usage: 
python modelling/eval_model.py -d data/early_data.csv -o data/models/earlydata -g data/models/ldagridsearch_earlydata.pkl
python modelling/eval_model.py -d data/late_data.csv -o data/models/latedata -g data/models/ldagridsearch_latedata.pkl
python modelling/eval_model.py -d data/all_data.csv -o data/models/alldata -g data/models/ldagridsearch_alldata.pkl
'''
import pickle as pkl
from gen_model import LDA_model #load previous function for LDA
import pandas as pd
import argparse


def gen_best_LDA(best_df, df):
    category, topics, alpha, beta, __ = best_df.values[0]
    df_filt = df[df["category"] == category]
    
    model_dict = LDA_model(
        df = df_filt, 
        filters = (10, 0.5), 
        n = topics,
        beta = beta, 
        alpha = alpha, 
        only_coherence = False)

    filename = args['out_file'] + f'{category}.pkl'
    with open(filename, "wb") as f:
        pkl.dump(model_dict, f)

    print("Model Saved!")
    
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--data", required=True, help="path to data file")
    ap.add_argument("-o", "--out_file", required=True, help="path to output file")
    ap.add_argument("-g", "--gridsearch", required=True, help="path to gridsearch file")
    args = vars(ap.parse_args())
    with open(args['gridsearch'], "rb") as f:
        data = pkl.load(f)

    ## Find best hyperparameters
    # media

    media = data[(data["Category"] == "Media")]
    best_media = media[media["Coherence"] == max(media["Coherence"])]

    # diplo

    diplo = data[(data["Category"] == "Diplomat")]
    best_diplo = diplo[diplo["Coherence"] == max(diplo["Coherence"])]

    # english text
    df = pd.read_csv(args['data'])
    df = df[df["retweet"] != "retweeted"]
    df['text_clean'] = df['text_clean'].astype(str)

    gen_best_LDA(best_media, df)
    gen_best_LDA(best_diplo, df)
