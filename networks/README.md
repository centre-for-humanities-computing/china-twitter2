# Network Analysis
Network analysis performed using the networkx package in python (https://networkx.org/) and the network visualizations are generated from the file ```network_main.py``` (see usage below). 
Nodes in the networks are Twitter handles, and edges (connections) are weighted by the number of mentions between the Twitter handles that are displayed. 
The network visualizations only plot Twitter handles that are either flagged as (i) Chinese diplomats or (ii) Chinese media outlets. 
The *edgewidth* (strength of connections) is determined by the number of mentions between Twitter handles of Chinese diplomats and media outlets (see below). 
The *nodesize* (size of handle) is determined by various attributes, such as: 
* *total mentions* (**Figure 2**): number of total mentions to the Twitter handle in question from all users (also non-diplomats and non-media that are not shown as nodes in the plot). This shows how "popular" the Chinese diplomats and media outlets are on Twitter broadly, rather than just their popularity/activity within the diplomat/media sub-network. 
* *weighted degree* (**Figure 3**): node-size scaled by number of total number of connections between Twitter handle in question and other Chinese diplomats and media outlets (both directions counted, and each mention counted). The weighted degree plot corresponds to *in-degree* + *out-degree* (i.e. we count both directions). 
* *in-degree* (**Figure 4**): number of mentions from other Chinese diplomats and media outlets to the Twitter handle in question (only one direction counted). 
* *out-degree* (**Figure 5**): number of mentions from the Twitter handle in question to other Chinese diplomats and media outlets (only one direction counted). 

In addition to the network visualizations, we also show the top 10 handles (based on *weighted degree*) in **Figure 1**. The plot is generated in ```summary_stats_focus.py``` (see usage below). Clearly, some handles are primarily mentionees and have high *in-degree* (e.g. CHNews) while others are primarily mentioners and have high *out-degree* (e.g. zlj517) within the diplomat/media sub-network. 

## Usage:
1. Activate environment

```
source cnenv/bin/activate
```

2. Navigate to the network code folder
```
cd networks/src
```

3. Run bash script 

```
bash preprocessing.sh 
```

This bash script calls the ```concat_files.py``` file which concatenates a directory of .csv files to one .csv file. 

4. Run python file 

```
python subsets.py 
```

This subsets the data into three periods: </br>
(1) early period: 01.11.19-28.02.21 </br>
(2) late period: 01.03.21-30.04.22 </br>
(3) full period: 01.11.19-30.04.22 </br> 

5. Run python file

```
python data_cleaning.py 
```

This fixes data issues and inconsistencies. 

6. Run bash script

```
bash network_early.sh
bash network_late.sh
bash network_full.sh
```

in the scripts above set: <br/>
```NET=true``` <br/>
```SUM=true``` <br/>

This runs the main analysis (network plots and summary statistics). 

7. Run python file

```
python influencers.py
```

This generates plot and overview over the mentions from influencers to handles belonging to Chinese diplomats and media outlets. 