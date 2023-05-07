import pandas as pd 
import re
import seaborn as sns 
import matplotlib.pyplot as plt
import openpyxl

# set vars
outpath = "/work/cn-some/china-twiplomacy-2020-2022/networks/fig/influencers"

# main data
d = pd.read_csv("/work/cn-some/china-twiplomacy-2020-2022/networks/data/clean/full_clean.csv")
d.head(5)

# influencers
with open('/work/cn-some/china-twiplomacy-2020-2022/networks/data/reference/influencers.txt') as f:
    lines = f.readlines()

lines = [re.sub(r'\n', '', x) for x in lines]
d_influencers = pd.DataFrame({'mentioner': lines})

# join 
d_merged = d.merge(d_influencers, on = "mentioner", how = "inner")
d_merged.to_csv(f"{outpath}/influencer_overview.csv", index=False)
d_xlsx = d_merged[["created_at", "mentionee", "mentioner", "retweet", "category_mentionee", "text"]]
d_xlsx.to_excel(f'{outpath}/influencer_overview.xlsx', sheet_name = "influencers", index=False)

# generate csv file & write
d_overview = d_merged.groupby('mentionee').size().reset_index(name = 'number_influencer_mentions').sort_values('number_influencer_mentions', ascending=False)
d_overview.to_csv(f"{outpath}/influencer_grouped.csv", index=False)

## plot over time ## 
d_merged["created_at"] = pd.to_datetime(d_merged["created_at"]).dt.date

##### overall 
def plot_overall(d, outpath, outname): 
    d = d.sort_values('created_at', ascending=True).reset_index()
    d['cm'] = d.index + 1
    x = d['created_at']
    y = d['cm']

    fig, ax = plt.subplots(dpi=150) # tweak figsize potentially 
    plt.fill_between(x, y)
    ax.xaxis.set_major_locator(plt.MaxNLocator(4))
    plt.title('Mentions by Influencers')
    plt.xlabel('Date')
    plt.ylabel('Mentions (cumulative)')
    plt.savefig(f"{outpath}/{outname}", bbox_inches='tight')

plot_overall(d_merged, outpath, "cumulative_mentions.png")

##### by top accounts
def plot_top_n(d, n, outpath, outname): 
    d_sorted = d.groupby('mentionee').size().reset_index(name = 'count').sort_values('count', ascending=False).head(n)
    d_filtered = d.merge(d_sorted, on = "mentionee", how = "inner")
    print(f"total mentions: {len(d)}")
    print(f"mentions to top-{n}: {len(d_filtered)}")
    d_filtered = d_filtered.sort_values('created_at', ascending=True)
    d_filtered['cumsum'] = d_filtered.groupby('mentionee').cumcount()+1
    d_filtered = d_filtered.rename(columns = {'mentionee': 'handle'})
    fig, ax = plt.subplots(dpi=150)
    sns.lineplot(
        x = 'created_at',
        y = 'cumsum',
        hue = 'handle',
        data = d_filtered)
    ax.xaxis.set_major_locator(plt.MaxNLocator(4))
    plt.title(f'Mentions by Influencers (top {n} handles)')
    plt.xlabel('Date')
    plt.ylabel('Mentions (cumulative)')
    plt.savefig(f"{outpath}/{outname}", bbox_inches="tight")

plot_top_n(d_merged, 5, outpath, "cumulative_top5.png")