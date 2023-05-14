import sys
from pathlib import Path
sys.path.append(str(Path.cwd().parent / "src" ))
from helper_functions import load_models, visualize_model, topics_over_time, prep_data, plot_subset
from pyLDAvis import save_html


def main():
    path = Path(__file__)

    mdl_path = path.parents[1] / 'mdl'
    fig_path = path.parents[1] / 'fig'
    data_path = path.parents[2] / 'data'

    # ensure that fig path exists
    if not fig_path.exists():
        fig_path.mkdir(parents=True)

    # load model
    for period in ["early", "late", "all"]:
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

if __name__ == '__main__':
    main()