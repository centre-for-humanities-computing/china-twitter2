# china-twitter2

## Dataset

### Diplomacy

### Media

## Topic analysis
A topic model was created for each of the three time periods. Latent Dirichlet Allocation topic modelling using `gensim` package in Python (See documentation: https://radimrehurek.com/gensim_3.8.3/models/ldamodel.html). 
LDA is a hierarchical Bayesian model with three levels, in which each item of a collection, in this case tweets, is modeled as a finite mixture over an underlying set of topics. In turn, each topic is modeled as an infinite mixture over an underlying set of topic probabilities. An explicit representation of each tweet is provided by the topic probabilities. 

A total of 180 models were trained for both diplomat and media tweets in each time period with a variation of the following three hyperparameters:
* Number of Topics (K)
    * The topic model was trained requesting 10, 15, 20, 25, 30 and 35 latent topics
* Dirichlet hyperparameter alpha: A-priori document-topic density
    * The topic model was trained using 6 different a-priori beliefs about the document-topic density, including 0.01, 0.31, 0.61, 0.91, symmetric ![equation](https://latex.codecogs.com/svg.image?%5Cleft(%5Cfrac%7B1%7D%7Bn_%7Btopics%7D%7D%5Cright)) and asymmetric ![equation](https://latex.codecogs.com/svg.image?%5Cleft(%5Cfrac%7B1%7D%7Btopic_%7Bi%7D%20&plus;%20%5Csqrt%7Bn_%7Btopics%7D%7D%7D%5Cright))
* Dirichlet hyperparameter beta: A-priori word-topic density
    * The topic model was trained using 5 different a-priori beliefs about the word-topic density, including 0.01, 0.31, 0.61, 0.91 and symmetric ![equation](https://latex.codecogs.com/svg.image?%5Cleft(%5Cfrac%7B1%7D%7Bn_%7Btopics%7D%7D%5Cright))

The model with the best ![equation](https://latex.codecogs.com/svg.image?c_v) coherence score is chosen for analysis.

## Network analysis
Network analysis performed using the networkx package in python (https://networkx.org/) and the network visualizations are generated from the file ```network_main.py``` (see usage below). 
Nodes in the networks are Twitter handles, and edges (connections) are weighted by the number of mentions between the Twitter handles that are displayed. 
The network visualizations only plot Twitter handles that are either flagged as (i) Chinese diplomats or (ii) Chinese media outlets. 
The *edgewidth* (strength of connections) is determined by the number of mentions between Twitter handles of Chinese diplomats and media outlets (see below). 
The *nodesize* (size of handle) is determined by various attributes, such as: 
* *total mentions* (**Figure 2**): number of total mentions to the Twitter handle in question from all users (also non-diplomats and non-media that are not shown as nodes in the plot). This shows how "popular" the Chinese diplomats and media outlets are on Twitter broadly, rather than just their popularity/activity within the diplomat/media sub-network. 
* *weighted degree* (**Figure 3**): node-size scaled by number of total number of connections between Twitter handle in question and other Chinese diplomats and media outlets (both directions counted, and each mention counted). The weighted degree plot corresponds to *in-degree* + *out-degree* (i.e. we count both directions). 
* *in-degree* (**Figure 4**): number of mentions from other Chinese diplomats and media outlets to the Twitter handle in question (only one direction counted). 
* *out-degree* (**Figure 5**): number of mentions from the Twitter handle in question to other Chinese diplomats and media outlets (only one direction counted). 

In addition to the network visualizations, we also show the top 10 handles (based on *weighted degree*) in **Figure 1**. The plot is generated in ```summary_stats_focus.py```.

## Sentiment analysis

## Use of photos and videos