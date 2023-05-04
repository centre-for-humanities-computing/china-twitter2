
import spacy
import pandas as pd
from transformers import pipeline
from tqdm import tqdm
import os
from pathlib import Path

nlp = pipeline("text-classification", model='bhadresh-savani/distilbert-base-uncased-emotion', top_k = None) # top_k = None returns all scores

def classify_emotions(df):
    """Classifies the emotions of the cleaned tweets.

    Args:
        df (pd.DataFrame): Dataframe containing the tweets to classify

    Returns:
        df (pd.DataFrame): Dataframe containing the classified tweets
    """

    df = df.reset_index()
    print('Classifying emotions from chunk')
    df['emotion'] = [nlp(tweet) if type(tweet)==str else '' for tweet in tqdm(df['text'])]
    
    # create a new column for each emotion
    for i in range(len(df['emotion'])):
        emotions = df['emotion'][i] # getting one row
        if emotions != '':
            for emotion in range(6): # getting one emotion
                emo = emotions[0][emotion]
                label = emo['label']
                prob = emo['score']
                df.loc[i, label] = prob
    return df

if __name__ == '__main__':
    path = Path(__file__)
    data_path = path.parents[2] / 'data'
    data = pd.read_csv(data_path / 'all_data_topic_model.csv')
    data = data[data['category'] == 'Diplomat']
    print(f'classifying diplomat data with {len(data)} rows')

    df = classify_emotions(data)
    df.to_csv(data_path / 'emotion_diplomat_data.csv', index=False)