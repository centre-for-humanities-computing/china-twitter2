'''
VMP 2022-06-09: check influencer behavior
'''

import pandas as pd 

# load actual data
df = pd.read_csv("/work/cn-some/china-twiplomacy-2020-2022/networks/data/clean/df_raw.csv")

# periods
#01.11.19-30.04.22 
#01.11.19-28.02.21 
#01.03.21-30.04.22 
total_start, total_end = "2019-11-01", "2022-04-30"
early_start, early_end = "2019-11-01", "2021-02-28"
late_start, late_end = "2021-03-01", "2022-04-30"

# filter dates
def filter_dates(df, start, end): 
    df_filtered = df[
        (df["created_at"] >= start) & 
        (df["created_at"] <= end)
    ]
    return df_filtered

df_total = filter_dates(df, total_start, total_end) 
df_early = filter_dates(df, early_start, early_end)
df_late = filter_dates(df, late_start, late_end)

len(df) # 37.565.160
len(df_total) # 26.079.893
len(df_early) # 15.013.341
len(df_late) # 11.066.552

## select useful columns for now 
select_cols = [
    'created_at',
    'mentionee',
    'mentioner',
    'retweet',
    'category',
    'category_mentionee',
    'text']

df_total = df_total[select_cols]
df_early = df_early[select_cols]
df_late = df_late[select_cols]

outpath = "/work/cn-some/china-twiplomacy-2020-2022/networks/data/clean"
df_total.to_csv(f"{outpath}/df_total.csv", index = False)
df_early.to_csv(f"{outpath}/df_early.csv", index = False)
df_late.to_csv(f"{outpath}/df_late.csv", index = False)
