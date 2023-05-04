"""
For summarizing the BERT emotion probabilities

Modified from emoDynamics (https://github.com/saraoe/emoDynamics)

usage: 
"""
import argparse
import pandas as pd
import numpy as np
import re
import ndjson
import time
import os
from typing import List


def emotion_distribution_mean(df):
    """
    Takes mean of each emotion probability of each emotion in a dataframe
    """
    emots = ["sadness", "joy", "anger", "fear", "surprise", "love"]
    return ([np.mean(df.loc[:, emot])  for emot in emots], [np.std(df.loc[:, emot]) for emot in emots])


def read_in_csv(filepath: str, time_col: str, tweets=True):
    ## load in data ##
    df = pd.read_csv(filepath)
    df["date"] = pd.to_datetime(df[time_col], utc=True).dt.strftime("%Y-%m-%d")

    return df


def write_ndjson_by_group(
    df: pd.DataFrame, group_by: List[str], filename: str):
    """
    Groups df by arguments in group_by list.
    Writes ndjson with group and emotion distribution

    Args
        df (pandas.DataFrame): Dataframe with the data
        group_by (List[str]): List of column to group by (e.g. date)
        filename (str): Name of the file to be written

    return
        None
    """
    grouped = df.groupby(group_by)
    for name, group in grouped:
        emo_prob, emo_prob_sd = emotion_distribution_mean(group)
        line = [
            {
                "group": name,
                "emo_prob": emo_prob,
                "emo_prob_sd": emo_prob_sd,
                "n": len(group),
            }
        ]
        with open(f"{filename}.ndjson", "a") as f:
            ndjson.dump(line, f)
            f.write("\n")


def main(filepath: str, time_col: str, rt: bool):
    df = read_in_csv(filepath, time_col=time_col)

    if rt == None: 
        df = df[df['retweet'] != 'retweeted']
        write_ndjson_by_group(
            df,
            group_by=["date"],
            filename=os.path.join('data', 'emotions_summarised', 'emotions_summarised_date_no_rt'),
        )
    
    else: 
        write_ndjson_by_group(
            df,
            group_by=["date"],
            filename=os.path.join('data', 'emotions_summarised', 'emotions_summarised_date'),
        )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--filepath",
        type=str,
        required=True,
        help="Path for the file containing the emotion scores",
    )
    parser.add_argument(
        "--time_col",
        type=str,
        required=True,
        help="The name of the column with time/date",
    )
    parser.add_argument(
        "--rt",
        type=bool,
        help="Whether to include retweets or not",
    )
    args = parser.parse_args()

    print(
        f"""Running summarise_emotions.py with:
             filepath={args.filepath},
             time_col={args.time_col},
             rt = {args.rt}"""
    )
    main(
        filepath=args.filepath,
        time_col=args.time_col,
        rt = args.rt
    )