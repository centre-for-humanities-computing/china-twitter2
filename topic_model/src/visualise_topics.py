import seaborn as sns
sns.set(style="whitegrid")
import sys
from pathlib import Path
sys.path.append(str(Path.cwd().parent / "src" ))
from helper_functions import *

# setting up matplotlib settings
# Source: https://towardsdatascience.com/making-matplotlib-beautiful-by-default-d0d41e3534fd
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import seaborn as sns
sns.set(style="whitegrid")
import pyLDAvis


def main():
    path = Path(__file__)

    mdl_path = path.parent / 'mdl'
    fig_path = path.parent / 'fig'

    # ensure that fig path exists
    if not fig_path.exists():
        fig_path.mkdir(parents=True)

    # load model
    for period in ["early", "late", "all"]:
        media_dict, diplo_dict = load_models(mdl_path / f'{period}dataMedia.pkl', mdl_path / '{period}dataDiplomat.pkl')
        diplo_vis = visualize_model(diplo_dict, sort_topics = False) 
        media_vis = visualize_model(media_dict, sort_topics = False)

    # save figures
    pyLDAvis.save_html(media_vis, fig_path / f"topic_model_media_{period}dates.html")
    pyLDAvis.save_html(diplo_vis, fig_path / f"topic_model_diplomat_{period}dates.html")

if __name__ == '__main__':
    main()