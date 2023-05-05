"""
Extracts wanted tweet for analysis in maxqda
"""

import pandas as pd
import openpyxl
import os
from pathlib import Path


def main():
    path = Path(__file__)
    data_path = path.parents[2] / "data" / "emotion_diplomat_data.csv"
    out_path = path.parents[1] / "excel"

    df = pd.read_csv(data_path)


    # January and forward subset
    # extract tweets joy and anger
    for emotion in ["joy", "anger"]:
        tmp_df = df.loc[(df['created_at'] > '2022-01-01')]
        tmp_df = tmp_df[['created_at', 'text', 'username', 'retweet', 'joy', 'love', 'anger', 'sadness', 'fear', 'surprise']]
        tmp_df = tmp_df[tmp_df[emotion]>0.8]
        tmp_df = tmp_df.sort_values(by = 'created_at').reset_index(drop = True)
        tmp_df.to_excel(out_path / f"{emotion}_tweets_from_jan2022.xlsx", index=False)
        
if __name__ == '__main__':
    main()