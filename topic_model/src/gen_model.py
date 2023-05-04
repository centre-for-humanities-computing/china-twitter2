'''
usage: 
python modelling/gen_model.py -i data/early_data.csv -o data/models/ldagridsearch_earlydata.pkl
python modelling/gen_model.py -i data/late_data.csv -o data/models/ldagridsearch_latedata.pkl
python modelling/gen_model.py -i data/all_data.csv -o data/models/ldagridsearch_alldata.pkl
'''

import gensim
import pandas as pd 
import pickle as pkl
import numpy as np 
import tqdm
import argparse
# Create Dictionary

def LDA_model(df, filters, n, beta, alpha, only_coherence = False):

    texts = [i.split() for i in df["text_clean"].values]

    id2word = gensim.corpora.Dictionary(texts)

    id2word.filter_extremes(filters[0], filters[1])
    
    # Term Document Frequency
    corpus = [id2word.doc2bow(doc) for doc in texts]


    lda_model = gensim.models.LdaMulticore(
        corpus=corpus,
        id2word = id2word,
        num_topics=n, 
        eta = beta, 
        alpha = alpha, 
        random_state=100,
        chunksize=100,
        passes = 10,
        per_word_topics=True)



    coherence_model_lda = gensim.models.CoherenceModel(
            model=lda_model, texts=texts, dictionary=id2word, coherence='c_v')

    coherence_score = coherence_model_lda.get_coherence()

    if only_coherence:
        return coherence_score

    return_dict = {
        "model": lda_model,
        "id2word": id2word,
        "corpus": corpus,
        "coherence": coherence_score
    }
    return return_dict

def grid_search(df, filename):
    # Topics range
    min_topics = 10
    max_topics = 40
    step_size = 5
    topics_range = range(min_topics, max_topics, step_size)
    total_topics = len(list(topics_range))

    # Alpha parameter
    alpha = list(np.arange(0.01, 1, 0.3))
    alpha.append('symmetric')
    alpha.append('asymmetric')
    total_alphas = len(alpha)

    # Beta parameter
    beta = list(np.arange(0.01, 1, 0.3))
    beta.append('symmetric')
    total_beta = len(beta)

    model_results = {
        'Category': [],
        'Topics': [],
        'Alpha': [],
        'Beta': [],
        'Coherence': []
        }
    # Can take a long time to run

    # Categories
    categories = ['Media']#["Media", "Diplomat"]
    total_categories = len(categories)
    
    pbar = tqdm.tqdm(total=total_topics * total_alphas * total_beta * total_categories)
    
    #iterate through categories
    for i in categories:
        df_filt = df[df["category"] == i]
        # iterate through validation corpuses
        for k in topics_range:
            # iterate through alpha values
            for a in alpha:
                # iterare through beta values
                for b in beta:
                    # get the coherence score for the given parameters
                    cv = LDA_model(df = df_filt, 
                    filters = (10, 0.5), 
                    n = k, 
                    beta = b, 
                    alpha = a, 
                    only_coherence = True)

                    # Save the model results
                    model_results['Category'].append(i)
                    model_results['Topics'].append(k)
                    model_results['Alpha'].append(a)
                    model_results['Beta'].append(b)
                    model_results['Coherence'].append(cv)
                    
                    pbar.update(1)
    data = pd.DataFrame(model_results)
    with open(filename, "wb") as f:
            pkl.dump(data, f)
    pbar.close()

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--in_file", required=True, help="path to data file")
    ap.add_argument("-o", "--out_file", required=True, help="path to output file")
    args = vars(ap.parse_args())
    df = pd.read_csv(args['in_file'])
    df = df[df["retweet"] != "retweeted"]
    df['text_clean'] = df['text_clean'].astype(str)
    grid_search(df, args['out_file'])