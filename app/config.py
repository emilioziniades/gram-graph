import os
from pathlib import Path


def in_data_dir(filename):
    return os.path.join(DATA_DIRECTORY, filename)


# hard coded for now
ACCOUNT = "happhoundsza"
PRUNE = True

DATA_DIRECTORY = os.path.join(Path(__file__).parents[1], "data")
PRUNED_FIGURE_FILENAME = in_data_dir("pruned_figure.json")
UNPRUNED_FIGURE_FILENAME = in_data_dir("unpruned_figure.json")
DATABASE_FILENAME = in_data_dir("followers.db")
SUMMARY_DATA_FILENAME = in_data_dir("follower_summary.json")
