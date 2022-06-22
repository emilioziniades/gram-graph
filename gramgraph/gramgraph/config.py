import os
from pathlib import Path


def in_data_dir(filename):
    return os.path.join(DATA_DIRECTORY, filename)


PROJECT_DIRECTORY = Path(__file__).parents[1]
DATA_DIRECTORY = os.path.join(Path(__file__).parents[2], "data")
PRUNED_FIGURE_FILENAME = in_data_dir("pruned_figure.json")
UNPRUNED_FIGURE_FILENAME = in_data_dir("unpruned_figure.json")
PICKLE_FILENAME = in_data_dir("followers.pickle")
DATABASE_FILENAME = in_data_dir("followers.db")
SUMMARY_DATA_FILENAME = in_data_dir("follower_summary.json")
