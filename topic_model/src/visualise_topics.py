import seaborn as sns
sns.set(style="whitegrid")
import sys
from pathlib import Path
sys.path.append(str(Path.cwd().parent / "src" ))
from helper_functions import load_models, visualize_model, topics_over_time, prep_data
from pyLDAvis import prepared_data_to_html, save_html

def plot_subset(df, range, legend_size, figname, figsize = (7.5, 4), dpi = 100): 
    fig, ax = plt.subplots(figsize = figsize, dpi = dpi)
    for topic in range: 
        df_tmp = df[df["topic_id"] == topic].sort_values(by = 'time')
        ax.plot(df_tmp['time'], df_tmp['average_weight'], label = f"Topic {topic}")
    ax.xaxis.set_major_locator(md.MonthLocator(interval = 2))
    ax.xaxis.set_major_formatter(md.DateFormatter('%b %y'))
    ax.set_ylim(bottom = 0, top = 0.4)
    ax.legend(frameon = True, loc = 'upper right', fontsize = legend_size)
    
    fig.savefig(f'plots/{figname}.png', bbox_inches = 'tight')

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
        #media_html = prepared_data_to_html(media_vis)
        #diplomat_html = prepared_data_to_html(diplo_vis)

        #save_html(media_vis, str(fig_path / f"topic_model_media_{period}dates.html"))
        #save_html(diplo_vis, str(fig_path / f"topic_model_diplomat_{period}dates.html"))
        
        # plot topics over time
        data, diplomats, media = prep_data(data_path / f"{period}_data_topic_model.csv")
        top_over_time = topics_over_time(diplo_dict, diplomats)

        #

if __name__ == '__main__':
    main()