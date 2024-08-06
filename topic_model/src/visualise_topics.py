import sys
from pathlib import Path
sys.path.append(str(Path.cwd().parent / "src" ))
from helper_functions import load_models, visualize_model, topics_over_time, prep_data, plot_subset
from pyLDAvis import save_html
import pandas as pd


def main():
    path = Path(__file__)

    mdl_path = path.parents[1] / 'mdl'
    fig_path = path.parents[1] / 'fig'
    data_path = path.parents[2] / 'data'

    # ensure that fig path exists
    if not fig_path.exists():
        fig_path.mkdir(parents=True)

    # load model
    for period in ["all", "early", "late"]:
        media_dict, diplo_dict = load_models(mdl_path / f'{period}dataMedia.pkl', mdl_path / f'{period}dataDiplomat.pkl')
        
        diplo_vis = visualize_model(diplo_dict, sort_topics = False) 
        media_vis = visualize_model(media_dict, sort_topics = False)

        # save figures
        save_html(media_vis, str(fig_path / f"topic_model_media_{period}dates.html"))
        save_html(diplo_vis, str(fig_path / f"topic_model_diplomat_{period}dates.html"))

        # plot topics over time
        data, diplomats, media = prep_data(data_path / f"{period}_data_topic_model.csv")
        top_over_time = topics_over_time(diplo_dict, diplomats)

        # depending on the number of topics, plot different subsets
        # plot 8 topics at a time
        n_topics = len(top_over_time.topic_id.unique())
        n_plots = n_topics // 8
    
        # plot 8 topics at a time
        for i in range(n_plots):
            plot_subset(top_over_time, range(8*i+1, 8*(i+1)+1), 10, str(fig_path / f"topics_over_time_{period}_{i}.png"))

        # plot the remaining topics
        if n_topics % 8 != 0:
            plot_subset(top_over_time, range(8*n_plots+1, n_topics), 10, str(fig_path / f"topics_over_time_{period}_{n_plots}.png"))
        
        # plot the clustered topics if period == all
        if period == "all":
            topic_cluster_mapping = {
                "A. China-foreign cooperation": [1, 10, 15], # three topics 
                "B. Ideological confrontation": [3, 4, 9, 13, 14, 21, 23,24,25, 27], # ten topics
                "C. China’s Achievements (economic, tech, infrastructure)": [5, 6, 8, 11, 20, 22, 26], # seven topics
                #"D. Party History": [17], # one topic (noted as r)
                #"E. State Stance on Global Affairs": [7, 14, 16], # three topics
                #"F. Covid 19": [12], # one topic
            }

            clustered_topics = pd.DataFrame()
            for cluster, topics in topic_cluster_mapping.items():
                # add together the topics in the cluster
                cluster_df = top_over_time[top_over_time.topic_id.isin(topics)]
                cluster_df["topic_id"] = cluster
                cluster_df = cluster_df.groupby(['month_year', 'topic_id']).sum(numeric_only=True).reset_index()
                clustered_topics = pd.concat([clustered_topics, cluster_df])

            # renaming for the plot
            clustered_topics['month_year'] = clustered_topics['month_year'].replace({
                '11_2019':'Nov 19', '12_2019':'Dec 19','1_2020':'Jan 20',
                '2_2020':'Feb 20', '3_2020':'Mar 20', '4_2020':'Apr 20',
                '5_2020':'May 20', '6_2020':'Jun 20', '7_2020':'Jul 20', 
                '8_2020':'Aug 20', '9_2020':'Sep 20', '10_2020':'Oct 20',
                '11_2020':'Nov 20', '12_2020':'Dec 20', '1_2021':'Jan 21', 
                '2_2021':'Feb 21', '3_2021': 'Mar 21', '4_2021': 'Apr 21',
                '5_2021':'May 21', '6_2021':'Jun 21', '7_2021':'Jul 21', 
                '8_2021':'Aug 21', '9_2021':'Sep 21', '10_2021':'Oct 21',
                '11_2021':'Nov 21', '12_2021':'Dec 21','1_2022':'Jan 22', 
                '2_2022':'Feb 22','3_2022': 'Mar 22','4_2022': 'Apr 22',
                '5_2022':'May 22', '6_2022':'Jun 22', '7_2022':'Jul 22', 
                '8_2022':'Aug 22', '9_2022':'Sep 22', '10_2022':'Oct 22',
                '11_2022':'Nov 22', '12_2022':'Dec 22'})
            
            clustered_topics['time'] = pd.to_datetime(clustered_topics['month_year'], format = '%b %y')

            # plot the cluster
            plot_subset(df = clustered_topics, 
                        range = topic_cluster_mapping.keys(), 
                        legend_size= 10, 
                        figname = str(fig_path / f"topics_over_time_{period}_cluster.png"),
                        ylim_top=0.6)


        

if __name__ == '__main__':
    main()