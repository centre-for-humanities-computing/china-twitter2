# Topic modelling
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


When the models have been generated, run the code in the topic_model.ipynb to visualize the results. Furthermore, visualisations of how prevalent each topic was over time (averaged topic weight) can be found in the `topics_over_time.ipynb`. 