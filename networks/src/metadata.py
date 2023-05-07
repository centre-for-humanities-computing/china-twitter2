'''
VMP 2022-06-13: meta-data for bot-detection in the other project (china-twitter)
'''

import pandas as pd 

# load stuff 
d = pd.read_csv("/work/cn-some/china-twiplomacy-2020-2022/networks/data/clean/df_raw.csv")
d = d[["created_at", "mentioner", "followers_mentioner", "following_mentioner"]]

# all dates 
def filter_dates(df, start, end): 
    df_filtered = df[
        (df["created_at"] >= start) & 
        (df["created_at"] <= end)
    ]
    return df_filtered

total_start, total_end = "2019-11-01", "2022-04-30"
df_total = filter_dates(d, total_start, total_end) 

# take most recent I guess
df_max = df_total.sort_values("created_at", ascending=False).groupby("mentioner", as_index=False).first()
df_max = df_max[["mentioner", "followers_mentioner", "following_mentioner"]]

# write file 
df_max.to_csv("/work/cn-some/china-twitter/bot-detection/curated_data/mentioner_fofo.csv", index = False)
