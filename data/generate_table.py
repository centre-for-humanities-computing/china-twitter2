"""
Generates table for README.md with information about the data
"""
import pandas as pd
from pathlib import Path
import pandas as pd 
import numpy as np
import datetime


def subset_dates(df, filter_dates=True):
    """
    Subsets the dataframe to only include dates between 2019-11-01 and 2022-04-30
    """

    df["created_at"] = pd.to_datetime(df["created_at"]).dt.tz_convert(None)  # Convert to timezone-naive datetime

    if filter_dates:
        start_date = pd.to_datetime(datetime.datetime(2019, 11, 1)).tz_localize(None)  # Convert start date to timezone-naive
        end_date = pd.to_datetime(datetime.datetime(2022, 4, 30)).tz_localize(None)  # Convert end date to timezone-naive

        df = df[
            (df["created_at"] >= start_date) &
            (df["created_at"] <= end_date)
        ]


    return df

def unique_users(df):
    """
    Finds the unique users in the dataframe both media and diplomats
    """

    diplomats = df[df["category"] == "Diplomat"]["username"].unique()
    media = df[df["category"] == "Media"]["username"].unique()

    return diplomats, media


def get_information_user(user, df):

    # Subset to only include the user
    user_df = df[df["username"] == user]

    # Get the number of original tweets
    original_tweets = user_df[user_df["retweet"] != "retweeted"]

    # Original tweets in English
    original_tweets_en = original_tweets[original_tweets["language"] == "en"]

    # Retweets
    retweets = user_df[user_df["retweet"] == "retweeted"]

    # Retweets in English
    retweets_en = retweets[retweets["language"] == "en"]

    # create dataframe with information
    information = pd.DataFrame(
        {
            "Original tweets": [len(original_tweets)],
            "Original tweets in English": [len(original_tweets_en)],
            "Retweets": [len(retweets)],
            "Retweets in English": [len(retweets_en)],
            "Total": [len(user_df)]
        }
    )

    return information


    


def main():

    path = Path(__file__)
    data_path = path / "raw_data.csv"

    df = pd.read_csv(data_path)

    df = subset_dates(df)

    diplo_users, media_users = unique_users(df)
        
    print(f"Number of unique users: {len(diplo_users) + len(media_users)}")
    print(f"Number of unique diplomats: {len(diplo_users)}")
    print(f"Number of unique media: {len(media_users)}")

    diplo_table = pd.DataFrame(columns=["Original tweets", "Original tweets in English", "Retweets", "Retweets in English", "Total"])
    
    for user in diplo_users:
        information = get_information_user(user, df)
        diplo_table = diplo_table.append(information)

    save_path = path / "diplo_table.csv"
    diplo_table.to_csv(save_path, index=False)




    

if __name__ == "__main__":

    main()