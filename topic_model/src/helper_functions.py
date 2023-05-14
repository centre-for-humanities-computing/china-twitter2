import pandas as pd 
import pickle as pkl 
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.dates as md
import pyLDAvis.gensim as gm
import pyLDAvis
import re
from tqdm import tqdm

plt.rcParams['font.family'] = 'serif'
plt.rcParams['figure.titlesize'] = 20
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.dpi'] = 300


color_list = ["#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7", "#800080", "#FFA500", "#00FF00", "#FF0000", "#FFFF00"]


### MAKE FUNCTIONS

def prep_data(filepath):
    """Preparing the data

    Returns:
        pd.Dataframes: Returns three dataframes - the whole dataset, the diplomats and the media.
    """    
    en_df = pd.read_csv(filepath)

    en_df['month'] = pd.DatetimeIndex(en_df['created_at']).month
    en_df['date'] = pd.DatetimeIndex(en_df['created_at']).date
    
    
    def retweet_binary(string):
        if string == "retweeted":
            return "Retweet"
        else:
            return "Other"

    en_df["retweet_bin"] = en_df["retweet"].apply(lambda x: retweet_binary(x))
    
    en_df["date"] = pd.to_datetime(en_df["date"])
    
    return en_df, en_df[en_df["category"] == "Diplomat"].reset_index(drop=True), en_df[en_df["category"] == "Media"].reset_index(drop=True)
    
def available_users(data):
    """Function for listing the available users.

    Args:
        data (pd.DataFrame): Data for which the user wants a list of users to use for "options".

    Returns:
        list: list of usernames from the data
    """    
    return list(set(data["username"]))



# Find the topic number with the highest 
def dominant_topic(ldamodel, corpus, document, save_name = ""):
    '''
    Creates a dataframe, which indicates the dominant topic
    of a given document. 
    ___
    Examples:
    ___
    df_dominant = dominant_topic(models[model_name], corpus, df["org_text"])
    '''
    # init dataframe
    topics_df = pd.DataFrame()

    # GET MAIN TOPIC IN EACH DOCUMENT
    # Get through the pages
    for num, doc in enumerate(tqdm(ldamodel[corpus])):
        # Count number of list into a list
        if sum(isinstance(i, list) for i in doc)>0:
            doc = doc[0]

        doc = sorted(doc, key= lambda x: (x[1]), reverse=True)
    
        for j, (topic_num, prop_topic) in enumerate(doc):
            if j == 0: # => dominant topic
                # Get list prob. * keywords from the topic
                pk = ldamodel.show_topic(topic_num)
                topic_keywords = ', '.join([word for word, prop in pk])
                # Add topic number, probability, keywords and original text to the dataframe
                topics_df = topics_df.append(pd.Series([int(topic_num), np.round(prop_topic, 4),
                                                    topic_keywords, document[num]]),
                                                    ignore_index=True)
            else:
                break
                
    # Add columns name
    topics_df.columns = ['Dominant_Topic', 'Topic_Perc_Contribution', 'Keywords', 'Text']

    if save_name:
        with open(f"data/dominant_dfs/{save_name}.pkl", "wb") as f: 
            pkl.dump(topics_df, f)

    return topics_df

def load_dominant_dfs():
    with open(f"data/dominant_dfs/diplo_dominant.pkl", "rb") as f: 
        diplo = pkl.load(f)
        
    with open(f"data/dominant_dfs/media_dominant.pkl", "rb") as f: 
        media = pkl.load(f)
    
    return diplo, media

def topic_threshold(df, topic, threshold):
    '''
    Creates a subset of the data, which is documents that 
    have a topic_perc_contribution over a set threshold.
    '''
    return df[(df["Dominant_Topic"] == topic) & (df["Topic_Perc_Contribution"] > threshold)].sort_values("Topic_Perc_Contribution", ascending = False)

def query_topic(data, sub_size, query, topic = False):
    '''
    Queries a dataframe and gives a subset of sub_size length.
    This query contains both the topic and a query string. 
    Alternatively, setting topic = False only queries the dataframe
    and returns the sorted dataframe.
    '''
    if topic:
        data = data[(data["Text"].str.contains(query)) & (data["Dominant_Topic"] == topic)]
    else:
        data = data[data["Text"].str.contains(query)]
    return data.sort_values("Topic_Perc_Contribution", ascending=False).head(sub_size)


def topic_names(models, k): 
    """Function for going through all topics and labelling them

    Args:
        models (LDA Model): Topic Model
        k (int): Number of topics to go through

    Returns:
        list: list containing the labels for each topic
    """    

    liste = [] 

    for i in range(k): 
        (models.print_topic(i, 10))
        label = input("Topic Label: ")
        liste.append(label)
        print(liste)

    return liste

def load_models(mediapath, diplomatpath):
    with open(mediapath, "rb") as f:
        media = pkl.load(f)
    
    with open(diplomatpath, "rb") as f:
        diplo = pkl.load(f)
        
    return media, diplo

def visualize_model(dictionary, sort_topics = False):
    #Creating Topic Distance Visualization 
    p = gm.prepare(dictionary["model"], dictionary["corpus"], dictionary["id2word"], sort_topics = sort_topics)
    return p

def topics_over_time(lda, data):
    # code adapted from https://jeriwieringa.com/2017/06/21/Calculating-and-Visualizing-Topic-Significance-over-Time-Part-1/
    
    distribution = []
    for i in range(len(lda['corpus'])):
        distribution.append(lda['model'][lda['corpus']][i])
        
    no_retweets = data[data["retweet"] != "retweeted"].reset_index(drop = True)
    no_retweets = no_retweets[["text", "created_at"]]
    
    probs = lda['model'].get_document_topics(lda['corpus'], minimum_probability=0, minimum_phi_value=None, per_word_topics=False)

    probsdf = pd.DataFrame(probs)


    for i in range(probsdf.shape[0]):
        for n in range(probsdf.shape[1]):
            probsdf.loc[i, n] = probsdf.loc[i, n][1]
            
    probsdf = probsdf.apply(pd.to_numeric)
    probsdf['topic_weight'] = probsdf.max(axis=1)
    probsdf['topic_id'] = probsdf.idxmax(axis=1)
    
    tweetsandprobs = pd.concat([no_retweets, probsdf], axis=1, join="inner")
    
    # Getting the month and year of each post
    tweetsandprobs['month'] = pd.DatetimeIndex(tweetsandprobs['created_at']).month.astype('str')
    tweetsandprobs['year'] = pd.DatetimeIndex(tweetsandprobs['created_at']).year.astype('str')
    tweetsandprobs['month_year'] = tweetsandprobs['month'] +'_'+  tweetsandprobs['year']
    
    tweetsandprobs = tweetsandprobs.drop(columns=['month', 'year', 'topic_weight', 'topic_id'])
    tweetsandprobs = tweetsandprobs.melt(id_vars =['month_year', 'text', 'created_at'], var_name='topic_id', value_name='topic_weight')
    
    # Grouping by each month in each year to get the total docs column
    total_docs = tweetsandprobs.groupby('month_year')['text'].apply(lambda x: len(x.unique())).reset_index()
    total_docs.columns = ['month_year', 'total_docs']
    
    # Group by year and topic id
    df_avg = tweetsandprobs.groupby(['month_year', 'topic_id']).agg({'topic_weight': 'sum'}).reset_index()
    df_avg = df_avg.merge(total_docs, on="month_year", how="left")
    df_avg['average_weight'] = df_avg['topic_weight'] / df_avg['total_docs']
    
    # renaming for the plot
    df_avg['month_year'] = df_avg['month_year'].replace({
    '11_2019':'Nov 19',
    '12_2019':'Dec 19',
    '1_2020':'Jan 20',
    '2_2020':'Feb 20', 
    '3_2020':'Mar 20', 
    '4_2020':'Apr 20',
    '5_2020':'May 20',
    '6_2020':'Jun 20',
    '7_2020':'Jul 20', 
    '8_2020':'Aug 20', 
    '9_2020':'Sep 20', 
    '10_2020':'Oct 20',
    '11_2020':'Nov 20',
    '12_2020':'Dec 20',
    '1_2021':'Jan 21', 
    '2_2021':'Feb 21',
    '3_2021': 'Mar 21',
    '4_2021': 'Apr 21',
    '5_2021':'May 21',
    '6_2021':'Jun 21',
    '7_2021':'Jul 21', 
    '8_2021':'Aug 21', 
    '9_2021':'Sep 21', 
    '10_2021':'Oct 21',
    '11_2021':'Nov 21',
    '12_2021':'Dec 21',
    '1_2022':'Jan 22', 
    '2_2022':'Feb 22',
    '3_2022': 'Mar 22',
    '4_2022': 'Apr 22',
    '5_2022':'May 22',
    '6_2022':'Jun 22',
    '7_2022':'Jul 22', 
    '8_2022':'Aug 22', 
    '9_2022':'Sep 22', 
    '10_2022':'Oct 22',
    '11_2022':'Nov 22',
    '12_2022':'Dec 22'
     })
    
    df_avg['time'] = pd.to_datetime(df_avg['month_year'], format = '%b %y')
    df_avg['topic_id'] = df_avg['topic_id']+1
    
    return df_avg

def plot_subset(df, range, legend_size, figname, figsize = (10, 6), dpi = 300): 
    fig, ax = plt.subplots(figsize = figsize, dpi = dpi)
    for i, topic in enumerate(range): 
        df_tmp = df[df["topic_id"] == topic].sort_values(by = 'time')
        ax.plot(df_tmp['time'], df_tmp['average_weight'], label = f"Topic {topic}", color = color_list[i])
    ax.xaxis.set_major_locator(md.MonthLocator(interval = 2))
    ax.xaxis.set_major_formatter(md.DateFormatter("%b-%Y"))
    for label in ax.get_xticklabels():
        label.set_ha("right")
        label.set_rotation(45)
    ax.set_ylim(bottom = 0, top = 0.4)
    ax.legend(frameon = True, loc = 'upper right', fontsize = legend_size)
    
    fig.savefig(figname, bbox_inches = 'tight')
    
    