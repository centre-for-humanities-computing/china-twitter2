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

    diplomats.sort()
    media.sort()

    return diplomats, media


def get_information_user(user, df):

    # Subset to only include the user
    user_df = df[df["username"] == user]

    # Get the number of original tweets
    original_tweets = user_df[user_df["retweet"] != "retweeted"]

    # Original tweets in English
    original_tweets_en = original_tweets[original_tweets["lang"] == "en"]

    # Retweets
    retweets = user_df[user_df["retweet"] == "retweeted"]

    # Retweets in English
    retweets_en = retweets[retweets["lang"] == "en"]

    # create dataframe with information
    information = pd.DataFrame(
        {
            "User": [user], 
            "Original tweets": [len(original_tweets)],
            "Original tweets in English": [len(original_tweets_en)],
            "Retweets": [len(retweets)],
            "Retweets in English": [len(retweets_en)],
            "Total": [len(user_df)]
        }
    )

    return information


def generate_table(users, df):
    table = pd.DataFrame()
    
    for user in users:
        information = get_information_user(user, df)
        table = pd.concat([table, information])

    return table


def main():
    path = Path(__file__)
    data_path = path.parents[0] / "raw_data.csv"

    df = pd.read_csv(data_path)

    df = subset_dates(df)

    diplo_users, media_users = unique_users(df)
    print(media_users)
        
    print(f"Number of unique users: {len(diplo_users) + len(media_users)}")
    print(f"Number of unique diplomats: {len(diplo_users)}")
    print(f"Number of unique media: {len(media_users)}")

    for user_list, filename in zip([diplo_users, media_users], ["diplo_table.csv", "media_table.csv"]):
        table = generate_table(user_list, df)
        save_path = path.parents[0] / filename
        table.to_csv(save_path, index=False)

        # print markdown table
        print(table.to_markdown(index=False))



    

if __name__ == "__main__":

    main()