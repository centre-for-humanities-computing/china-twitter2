"""
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mtpl
import matplotlib.dates as mdates
import os
from pathlib import Path
from math import log

mtpl.rcParams['font.family'] = 'serif'
mtpl.rcParams['figure.titlesize'] = 20
mtpl.rcParams['axes.labelsize'] = 14
mtpl.rcParams['xtick.labelsize'] = 10
mtpl.rcParams['ytick.labelsize'] = 10
mtpl.rcParams['legend.fontsize'] = 10
mtpl.rcParams['figure.dpi'] = 300

palette = ["#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7"]
locator = mdates.MonthLocator()  # every month
date_form = mdates.DateFormatter("%b-%Y")

def return_counts(data, measure):
    """
    Returns the number of tweets or retweets per day.
    """
    if measure == 'tweets':
        counts = data['created_at'].groupby(data['created_at']).count()
    elif measure == 'retweets':
        # sum the number of retweets per day
        counts = data['retweet_count'].groupby(data['created_at']).sum()
    
    return counts

def plot_ax(tweets, ax, measure):
    """
    Plots the number of tweets or retweets per day.
    """

    # get the counts per day (either tweets or retweets)
    counts = return_counts(tweets, measure)
    
    # plot the values
    ax.plot(counts.index, counts.values, linewidth = 1, alpha = 0.5)

    # plot a smoothed version of the data
    gaussian = counts.rolling(window=50, win_type='gaussian', center=True, min_periods=1).mean(std = 10)
    ax.plot(counts.index, gaussian, alpha=1, linewidth = 1, color = palette[4])

    # dates on the x-axis
    ax.xaxis_date()
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(date_form)

    # turn the labels on the x-axis 180 degrees and remove every second one
    for i, label in enumerate(ax.xaxis.get_ticklabels()):
        label.set_rotation(90)
        if i % 2 == 0:
            label.set_visible(False)

    return ax


def plot_joy_anger(data, ax):
    
    joy = data.groupby(['created_at'])['joy'].mean()
    anger = data.groupby(['created_at'])['anger'].mean()
    
    # plot the values
    ## joy
    ax.plot(joy.index, joy.values, linewidth = 1, alpha = 0.4, color = 'green')
    gaussian = joy.rolling(window=50, win_type='gaussian', center=True, min_periods=1).mean(std = 10)
    ax.plot(joy.index, gaussian, alpha=1, linewidth = 1, color = 'darkgreen')
    
    ## anger
    ax.plot(anger.index, anger.values, linewidth = 1, alpha = 0.4, color = 'red')
    gaussian = anger.rolling(window=50, win_type='gaussian', center=True, min_periods=1).mean(std = 10)
    ax.plot(anger.index, gaussian, alpha=1, linewidth = 1, color = 'darkred')
    

    # dates on the x-axis
    ax.xaxis_date()
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(date_form)

    # turn the labels on the x-axis 180 degrees and remove every second one
    for i, label in enumerate(ax.xaxis.get_ticklabels()):
        label.set_rotation(90)
        if i % 2 == 0:
            label.set_visible(False)

    return ax

def plot_all(data_list, title_list, lang = 'all', save_path = None):
    counter = -1
    fig, axs = plt.subplots(3, 3, figsize = (20, 10), sharex=True, sharey="row")
    
    for data in data_list:
        if lang != 'all': # only keep the data for the specified language
            data = data[data['lang'] == lang]
        
        # plot seperate plots for each category
        # add to the all in one plot
        counter += 1

        axs[0, counter] = plot_ax(data, axs[0, counter], measure = 'tweets')
        axs[1, counter] = plot_ax(data, axs[1, counter], measure = 'retweets')
        axs[2, counter] = plot_joy_anger(data, axs[2, counter])

    # set the titles of the plots
    for i, title in enumerate(title_list):
        axs[0, i].set_title(title, size = 15)

    axs[0, 0].set_ylabel('Number of tweets', size = 15)
    axs[1, 0].set_ylabel('Number of retweets', size = 15)

    # add a x-axis label to the whole figure
    fig.supxlabel('Date', size = 15)

    # prep title depending on language
    if lang == 'all':
        lang_info = 'all languages'
    else:
        lang_info = lang

    fig.suptitle(f'Original diplomat tweets ({lang_info})', size = 20)
    
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)



def plot_number_of_media_per_day(df, no_rt, figsize=(10, 10), media_type = 'photo', lang = None, save_path = None):
    '''Plots the number of tweets per day'''
    if lang != None:
        df = df[df['lang']==lang]
        no_rt = no_rt[no_rt['lang']==lang]

    no_rt = no_rt.groupby('created_at').mean(numeric_only=True).reset_index()
    df = df[df['retweet']=='retweeted']
    df = df.groupby('created_at').mean(numeric_only=True).reset_index()
    fig, ax = plt.subplots(1, 1, figsize=figsize)

    # only retweets
    ax.plot(df['created_at'], df[media_type], alpha = 0.2, color = palette[1])
    gaussian = df[media_type].rolling(window=20, win_type='gaussian', center=True, min_periods=1).mean(std = 3)
    if lang == None:
        ax.plot(df['created_at'], gaussian, color = palette[1], alpha=1, label = 'Retweeted by diplomats (all languages)')
    else:
        ax.plot(df['created_at'], gaussian, color = palette[1], alpha=1, label = f'Retweeted by diplomats ({lang})')
    # only original
    ax.plot(no_rt['created_at'], no_rt[media_type], alpha = 0.2, color = palette[2])
    gaussian = no_rt[media_type].rolling(window=20, win_type='gaussian', center=True, min_periods=1).mean(std = 3)
    if lang == None:
        ax.plot(no_rt['created_at'], gaussian, color = palette[2], alpha=1, label = 'All original diplomat tweets (all languages)')
    else: 
        ax.plot(no_rt['created_at'], gaussian, color = palette[2], alpha=1, label = f'All original diplomat tweets ({lang})')

    ax.legend()
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(date_form)

    ax.set_ylabel(f'Average number of {media_type}s per tweet')
    # turn xticks 90 degrees
    plt.setp(ax.get_xticklabels(), rotation=90, ha='center')
    if save_path:
        plt.savefig(save_path)

    plt.close()


if __name__ == '__main__':
    path = Path(__file__)

    data_path = path.parents[2] / "data" 
    fig_path = path.parents[1] / "fig"

    df = pd.read_csv(data_path / 'media_info.csv')
    df = df[df['category'] != 'Media']
    df['created_at'] = pd.to_datetime(df['created_at'], format = '%Y-%m-%d')
    df = df.sort_values(by='created_at')
    df_no_rt = df[df['retweet'] != 'retweeted']

    plot_number_of_media_per_day(df, df_no_rt, save_path= fig_path / "avg_photos.png")
    plot_number_of_media_per_day(df, df_no_rt, media_type = 'video', save_path= fig_path /" avg_videos.png")
    plot_number_of_media_per_day(df, df_no_rt, lang = 'en', save_path= fig_path /"avg_photos_en.png")
    plot_number_of_media_per_day(df, df_no_rt, media_type = 'video', lang = 'en', save_path= fig_path /"avg_videos_en.png")



    ## joined with emotions
        # read in the data
    df = pd.read_csv(data_path / 'media_info.csv')
    emo = pd.read_csv(data_path / 'emotion_diplomat_data.csv', usecols = ['tweetID', 'joy', 'love', 'anger', 'sadness', 'fear', 'surprise'])
    df = pd.merge(df, emo, how="inner", on = "tweetID")


    # merge
    # date time format
    df['created_at'] = pd.to_datetime(df['created_at'], format = '%Y-%m-%d')
    
    # only original diplomat tweets
    diplo_all = df[df['category'] == 'Diplomat'] 
    diplo_orig = diplo_all[diplo_all['retweet'] != 'retweeted']

    # only tweets with photos, videos, or neither
    diplo_orig_photos = diplo_orig[diplo_orig['photo'] != 0]
    diplo_orig_videos = diplo_orig[diplo_orig['video'] != 0]
    diplo_orig_text = diplo_orig.query('photo == 0 & video == 0')

    # all languages
    data_list = [diplo_orig_photos, diplo_orig_videos, diplo_orig_text]
    title_list = ['Tweets with photos', 'Tweets with videos', 'Tweets without photos or videos']
    plot_all(data_list, title_list, lang = 'all', save_path=fig_path / "orig_diplomat_tweets_rt_ntweets_time.png")

    # only English
    plot_all(data_list, title_list, lang = 'en', save_path=fig_path / "orig_diplomat_tweets_rt_ntweets_time_en.png")


    ### INVESTIGATING RETWEETS DIVIDED BY WITH MEDIA AND WITHOUT MEDIA (photos and videos)
    df = df[df['category'] != 'Media']
    df = df[df['retweet'] != 'retweeted']
    df['created_at'] = pd.to_datetime(df['created_at'], format = '%Y-%m-%d')
    df = df.sort_values(by='created_at')
    df_media = df.query('photo != 0 | video != 0')
    df_no_media = df.query('photo == 0 & video == 0')
    count_media = df_media.groupby("created_at")["tweetID"].count()
    count_no_media = df_no_media.groupby("created_at")["tweetID"].count()


    fig, ax = plt.subplots(1, 1, figsize=(20, 9))
    ax.plot(count_media, alpha = 0.3, color = palette[0])
    ax.plot(count_no_media, alpha = 0.3, color = palette[4])

    gaussian_media = count_media.rolling(window=20, win_type='gaussian', center=True, min_periods=1).mean(std = 3)
    gaussian_no_media = count_no_media.rolling(window=20, win_type='gaussian', center=True, min_periods=1).mean(std = 3)

    ax.plot(gaussian_media, alpha = 1, label = "Tweets with photos or videos",  color = palette[0])
    ax.plot(gaussian_no_media, alpha = 1, label = "Tweets without photos or videos", color =  palette[4])
    
    ax.xaxis.set_major_formatter(date_form)

    ax.set_ylabel('Number of tweets')

    ax.legend()
    plt.savefig(fig_path / "number_of_tweets.png")

    fig, ax = plt.subplots(2, 1, figsize=(15, 9), sharey=True)

    # plot the original tweets with images or videos
    for i, row in df_media.iterrows():
        if row['retweet_count'] != 0:
            ax[0].fill_between([row['created_at'], row['created_at'] + pd.Timedelta(days=1)], [0, 0], [log(row['retweet_count']), log(row['retweet_count'])], color=palette[4], alpha=0.01)
    ax[0].set_title('Original tweets with images or videos')
    ax[0].set_ylabel('Number of retweets (log)')
    ax[0].xaxis.set_major_formatter(date_form)


    # plot the original tweets without images or videos
    for i, row in df_no_media.iterrows():
        if row['retweet_count'] != 0:
            ax[1].fill_between([row['created_at'], row['created_at'] + pd.Timedelta(days=1)], [0, 0], [log(row['retweet_count']), log(row['retweet_count'])], color=palette[4], alpha=0.01)
    ax[1].set_title('Original tweets without images or videos')
    ax[1].set_ylabel('Number of retweets (log)')
    ax[1].xaxis.set_major_formatter(date_form)
    plt.savefig(fig_path / 'retweets.png', bbox_inches='tight')