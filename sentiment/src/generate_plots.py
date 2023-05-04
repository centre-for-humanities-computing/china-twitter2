import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib as mtpl
import pandas as pd
import os
import ruptures as rpt
import numpy as np
from pathlib import Path

#           1 orange  2 L blue   3 green    4 L orange  5 D blue  6 D orange 7 purple
palette = ["#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7"]

#palette = ['#911eb4', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#e6194b']
emotions =  ["sadness", "joy", "anger", "fear", "surprise", "love"]

mtpl.rcParams['font.family'] = 'serif'
mtpl.rcParams['figure.titlesize'] = 20
mtpl.rcParams['axes.labelsize'] = 14
mtpl.rcParams['xtick.labelsize'] = 10
mtpl.rcParams['ytick.labelsize'] = 10
mtpl.rcParams['legend.fontsize'] = 10
mtpl.rcParams['figure.dpi'] = 300

date_form = mdates.DateFormatter("%b-%Y")


##### PLOTTING FUNCTIONS #####

### Helper functions
def mark_date(ax, date, text = None, linestyle = '--', alpha = 0.5, color = 'black'):
    '''
    Marks a date on an ax with a vertical line.
    '''
    ax.axvline(x=pd.to_datetime(date, format = '%Y-%m-%d'), color=color, linestyle=linestyle, alpha=alpha)
    if text != None:
        ax.text(pd.to_datetime(date, format = '%Y-%m-%d'), 0.5, text, rotation=90, color=color, alpha=alpha)

    return ax
### Emotion functions

def plot_all_grid(df, save_path, figsize=(20, 10), normalize=True):
    """
    Plots the emotions of the tweets. One subplot for each emotion.
    """
    fig, axes = plt.subplots(2, 3, figsize=figsize, sharex=True, sharey=True)

    for i, ax in enumerate(axes.flatten()):
        if normalize: #min max normalisation
            emotion = (df[emotions[i]] - df[emotions[i]].min()) / (df[emotions[i]].max() - df[emotions[i]].min())
        else:
            emotion = df[emotions[i]]
        ax.plot(df['date_created'], emotion, color = palette[i], alpha=0.2)

        # plot smoothed line
        gaussian = emotion.rolling(window=50, win_type='gaussian', center=True, min_periods=1).mean(std = 3)
        ax.plot(df['date_created'], gaussian, color = palette[i], label = emotions[i], alpha=1)

        ax.xaxis_date()
        ax.xaxis.set_major_formatter(date_form)
        # turn xticks 90 degrees
        plt.setp(ax.get_xticklabels(), rotation=90, ha='center')
        ax.set_title(emotions[i])

    
    plt.savefig(save_path)
    plt.close()

def plot_emotions(df, save_path, figsize=(10, 6), normalize=True):
    """ 
    Plots the emotions of the tweets. One plot for all emotions.
    """
    fig, ax = plt.subplots(figsize=figsize)

    for i, emotion in enumerate(emotions):
        if normalize: #min max normalisation
            emotion = (df[emotion] - df[emotion].min()) / (df[emotion].max() - df[emotion].min())
            
        else:
            emotion = df[emotion]
            ax.plot(df['date_created'], emotion, color = palette[i], alpha=0.2)

        # plot smoothed line
        gaussian = emotion.rolling(window=50, win_type='gaussian', center=True, min_periods=1).mean(std = 3)
        ax.plot(df['date_created'], gaussian, color = palette[i], label = emotions[i], alpha=1)

    ax.xaxis_date()
    ax.xaxis.set_major_formatter(date_form)
    # turn xticks 90 degrees
    plt.setp(ax.get_xticklabels(), rotation=90, ha='center')
    ax.legend()
    
    plt.savefig(save_path)
    plt.close()

### Fluxis functions
def plot_fluxus(df, figsize=(10, 10), filename='fluxus.png', gaussian = False):
    """
    Plots transience, novelty and resonance
    """
    fig, axes = plt.subplots(3, 1, figsize=figsize, sharex=True)

    #sort by date
    df = df.sort_values(by='date')

    for i, ax in enumerate(axes.flatten()):
        if gaussian:
            alpha = 0.4
        else: 
            alpha = 1
        ax.plot(df['date'], df.iloc[:, 2+i], color = palette[3+i], alpha=alpha)

        if gaussian:
            gaus = df.iloc[:, 2+i].rolling(window=30, win_type='gaussian', center=True, min_periods=1).mean(std = gaussian)
            ax.plot(df['date'], gaus, color = palette[3+i], alpha=1)

        ax.xaxis_date()
        ax.xaxis.set_major_formatter(date_form)
        ax.set_title(df.columns[2+i].capitalize())
        ax.set_xlim([df['date'][0],df['date'][len(df['date'])-1]])
        

    plt.savefig(filename)
    plt.close()

### Change points 
def plot_change_points(flux, title, save_path, penalty = 2):
    
    fig, ax = plt.subplots(3, 1, figsize=(16,10), sharex=True)

    for ind, meas in enumerate(['novelty', 'resonance', 'transience']):
        mdl_emo = rpt.Pelt(model="rbf").fit(np.array(flux[meas]))
        shifts = mdl_emo.predict(pen=penalty)

        for i, shift in enumerate(shifts):
            if shift != shifts[-1]:
                if (i % 2) == 0:
                    color = palette[1]
                else:
                    color = palette[2]
                ax[ind].axvspan(flux['date'][shift-1], flux['date'][shifts[i+1]-1], facecolor = color, alpha = 0.1)

                if shift == shifts[0]: # making sure the time before the first shift also has a colour
                    ax[ind].axvspan(flux['date'][0], flux['date'][shift-1], facecolor = palette[1], alpha = 0.1)
        
        ax[ind].set_xlim([flux['date'][0],flux['date'][len(flux['date'])-1]])
        
        ax[ind].plot(flux['date'], flux[meas], color = 'k', linewidth = 1)
        ax[ind].set_title(meas.capitalize())

        ax[ind].xaxis_date()
        ax[ind].xaxis.set_major_formatter(date_form)

    # turn xticks 90 degrees
    plt.setp(ax[ind].get_xticklabels(), rotation=90, ha='center')
    plt.savefig(save_path)


### Other plots
def plot_number_of_tweets_per_day(rt, no_rt, figsize=(10, 10)):
    '''Plots the number of tweets per day'''
    fig, ax = plt.subplots(1, 1, figsize=figsize)

    ax.plot(rt['date_created'].value_counts().sort_index(), alpha = 0.2, color = palette[1])
    ax.plot(no_rt['date_created'].value_counts().sort_index(), alpha = 0.2, color = palette[0])

    # gaussian
    gaussian = rt['date_created'].value_counts().sort_index().rolling(window=20, win_type='gaussian', center=True, min_periods=1).mean(std = 3)
    ax.plot(gaussian, color = palette[1], alpha=1, label = 'All tweets')

    gaussian = no_rt['date_created'].value_counts().sort_index().rolling(window=20, win_type='gaussian', center=True, min_periods=1).mean(std = 3)
    ax.plot(gaussian, color = palette[0], alpha=1, label = 'No retweets')

    ax.legend()
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(date_form)
    # turn xticks 90 degrees
    plt.setp(ax.get_xticklabels(), rotation=90, ha='center')

    plt.savefig(os.path.join('fig', 'n_tweets.png'))
    plt.close()


if __name__ == '__main__':
    # Plotting emotions
    path = Path(__file__)
    
    data_path = path.parents[2] / "data" / "emotion_diplomat_data.csv"
    fig_path = path.parents[1] / "fig"

    df = pd.read_csv(data_path)
    df['date_created'] = pd.to_datetime(df['created_at'], format = '%Y-%m-%d')
    df = df.sort_values(by='date_created')

    df_no_rt = df[df['retweet'] != 'retweeted']

    # Plotting numbers of tweets each day
    plot_number_of_tweets_per_day(df, df_no_rt)

    for i, dat in enumerate([df, df_no_rt]):
        rt = ['', '_no_rt'][i]
        
        # average emotions over each day
        dat = dat.groupby('date_created').mean().reset_index()

        plot_all_grid(dat, save_path = fig_path / f'all_emotions{rt}_normalised.png', normalize=True)
        plot_all_grid(dat, save_path =fig_path / f'all_emotions{rt}.png', normalize=False)

        #plot_emotions(dat, fig_path / f'emotions{rt}_normalised.png', normalize=True)
        #plot_emotions(dat, fig_path / f'all_emotions{rt}_normalised.png', normalize=False)

        # may to nov
        dat_may = dat.loc[(dat['date_created'] < '2021-11-01') & (dat['date_created'] > '2021-04-30')]

        plot_all_grid(dat_may, save_path = os.path.join('fig', 'may_to_november', f'all_emotions{rt}_normalised.png'), normalize=True)
        plot_all_grid(dat_may, save_path = os.path.join('fig','may_to_november', f'all_emotions{rt}.png'), normalize=False)

        #plot_emotions(dat_may, f'fig/may_to_november/emotions{rt}_normalised.png', normalize=True)
        #plot_emotions(dat_may, f'fig/may_to_november/all_emotions{rt}_normalised.png', normalize=False)

        # after november
        dat_nov = dat.loc[(dat['date_created'] > '2021-11-01')]

        plot_all_grid(dat_nov, save_path = fig_path / 'nov' / f'all_emotions{rt}_normalised.png', normalize=True)
        plot_all_grid(dat_nov, save_path = fig_path / 'nov'/ f'all_emotions{rt}.png', normalize=False)

        #plot_emotions(dat_nov, f'fig/nov/emotions{rt}_normalised.png', normalize=True)
        #plot_emotions(dat_nov, f'fig/nov/all_emotions{rt}_normalised.png', normalize=False)


    # Plotting fluxus
    for i, file in enumerate(['emotions_summarised_date_no_rt', 'emotions_summarised_date']):
        flux = pd.read_csv(os.path.join('data', 'idmdl', f'{file}_W3.csv'))
        rt = ['_no_rt', ''][i]
        penalty = [1.5, 12][i]

        flux['date'] = pd.to_datetime(flux['date'], format = '%Y-%m-%d')
        flux = flux.sort_values(by='date')

        plot_fluxus(flux, filename = fig_path / f'fluxus{rt}.png', gaussian = [6, 40][i])
        flux = flux.reset_index(drop = True)

        # Variance shift points!
        plot_change_points(flux, penalty = penalty, title="Variance shift points in the emotion signal", save_path=f'fig/variance_shifts{rt}.png')

        # may to november
        flux_may = flux.loc[(flux['date'] < '2021-11-01') & (flux['date'] > '2021-04-30')]
        flux_may = flux_may.reset_index(drop = True)
        plot_change_points(flux_may, penalty = penalty, title="Variance shift points in the emotion signal", save_path=f'fig/may_to_november/variance_shifts{rt}.png')
        plot_fluxus(flux_may, filename = fig_path / f'may/fluxus{rt}.png')

        # november and forth
        flux_nov = flux.loc[(flux['date'] > '2021-11-01')]
        flux_nov = flux_nov.reset_index(drop = True)
        plot_change_points(flux_nov, penalty = penalty, title="Variance shift points in the emotion signal", save_path=f'fig/november_and_forth/variance_shifts{rt}.png')
        plot_fluxus(flux_nov, filename = fig_path /f'november/fluxus{rt}.png')



