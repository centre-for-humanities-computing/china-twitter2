'''
VMP 2022-06-09: sanity checks: 
(1) check that we have all diploamts
(2) check the types of values that we have in each column
'''

import pandas as pd 
import re 

# read main data
d_full = pd.read_csv("/work/cn-some/china-twiplomacy-2020-2022/networks/data/clean/df_total.csv")
d_early = pd.read_csv("/work/cn-some/china-twiplomacy-2020-2022/networks/data/clean/df_early.csv")
d_late = pd.read_csv("/work/cn-some/china-twiplomacy-2020-2022/networks/data/clean/df_late.csv")

# fix d problems (they are correctly called in "mentioner" column)
def fix_values(d): 
    d['mentionee'] = d['mentionee'].str.replace('ambcina', 'AmbCina')
    d['mentionee'] = d['mentionee'].str.replace('spokespersonHZM', 'SpokespersonHZM')
    return d 

d_full_clean = fix_values(d_full)
d_early_clean = fix_values(d_early)
d_late_clean = fix_values(d_late)

#### handles #####

# read handle information
with open('/work/cn-some/china-twiplomacy-2020-2022/networks/data/reference/complete.txt') as f:
    lines = f.readlines()

lines = [re.sub(r'\n', '', x) for x in lines]
d_handles = pd.DataFrame({'mentionee': lines})

# exclude everything not in the list of handles
d_full_inner = d_full_clean.merge(d_handles, on = "mentionee", how = "inner")
d_early_inner = d_early_clean.merge(d_handles, on = "mentionee", how = "inner")
d_late_inner = d_late_clean.merge(d_handles, on = "mentionee", how = "inner")

# how many handles now?
full_handles = list(d_full_inner['mentionee'].unique()) # all handles present (79 handles)
early_handles = list(d_early_inner["mentionee"].unique()) # many of them not in early (57 total)
late_handles = list(d_late_inner["mentionee"].unique()) # almost all in late period (78 total)

## save this information
def write_txt_file(lst, outpath, outname): 
    textfile = open(f"{outpath}{outname}.txt", "w")
    for element in lst:
        textfile.write(element + "\n")
    textfile.close()

outpath = "/work/cn-some/china-twiplomacy-2020-2022/networks/data/reference/"
write_txt_file(full_handles, outpath, "handles_full")
write_txt_file(early_handles, outpath, "handles_early")
write_txt_file(late_handles, outpath, "handles_late")

## fix status of the handles we now exclude
## they can still mention, but they should be "Neither" as category
focus_lst = ['ChinaEmbassyUSA', 'ConsulChinaBcn', 'zhu_jingyang', 'EUMissionChina', 'ChinaEmbEsp', 'ouzhounews']

def fix_excluded_handles(d, lst): 
    filter_cond = (d['mentioner'].isin(lst))
    d.loc[filter_cond, 'category'] = 'Neither'
    return d

#Neither
d_full_relabel = fix_excluded_handles(d_full_inner, focus_lst)
d_early_relabel = fix_excluded_handles(d_early_inner, focus_lst)
d_late_relabel = fix_excluded_handles(d_late_inner, focus_lst)

## check never mentioned by other diplomats?
# DIOC_MFA_China, ChinaCGMTL, XinWen_Ch, ChinaCG_HH, ChineseCon_Mel
# all mentioners are NEITHER (not diplomat or media)

## Fix that SpokespersonHZM should be "Diplomat" not "Neither"
def fix_hzm(d):
    filter_cond = (d['mentionee'] == "SpokespersonHZM")
    d.loc[filter_cond, 'category_mentionee'] = 'Diplomat'
    return d 

d_full_hzm = fix_hzm(d_full_relabel)
d_early_hzm = fix_hzm(d_early_relabel)
d_late_hzm = fix_hzm(d_late_relabel)

## check that all categories are correct
with open('/work/cn-some/china-twiplomacy-2020-2022/networks/data/reference/diplomats.txt') as f:
    lines = f.readlines()

lines = [re.sub(r'\n', '', x) for x in lines]
diplomats = pd.DataFrame({'mentionee': lines})

with open('/work/cn-some/china-twiplomacy-2020-2022/networks/data/reference/media.txt') as f:
    lines = f.readlines()

lines = [re.sub(r'\n', '', x) for x in lines]
media = pd.DataFrame({'mentionee': lines})

d_full_hzm_diplomats = d_full_hzm.merge(diplomats, on = "mentionee", how = "inner")
d_full_hzm_media = d_full_hzm.merge(media, on = "mentionee", how = "inner")

d_full_hzm_diplomats.groupby('category_mentionee').size() # good
d_full_hzm_media.groupby('category_mentionee').size() # good

## save the main dataframes 
outpath = "/work/cn-some/china-twiplomacy-2020-2022/networks/data/clean/"
d_full_hzm.to_csv(f"{outpath}full_clean.csv", index=False)
d_early_hzm.to_csv(f"{outpath}early_clean.csv", index=False)
d_late_hzm.to_csv(f"{outpath}late_clean.csv", index=False)