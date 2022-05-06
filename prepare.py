import os
import json
import pickle
from typing import Tuple

from graph import GramGraph, test_data

import plotly

""" Converts followers data into pruned and unpruned data"""


def main():
    pruned_JSON, unpruned_JSON = get_figures_JSON()

    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    for json_file, filename in [
        (pruned_JSON, "pruned_figure.json"),
        (unpruned_JSON, "unpruned_figure.json"),
    ]:
        with open(os.path.join(data_dir, filename), "w") as f:
            f.write(json_file)


def get_figures_JSON() -> Tuple[str, str]:
    """Preloads JSON for both pruned and unpruned graphs"""
    with open("followers.pickle", "rb") as f:
        followers = pickle.load(f)
    G = GramGraph(followers, prune=False)
    GP = GramGraph(followers, prune=True)
    unpruned_fig = G.plot_graph()
    pruned_fig = GP.plot_graph()
    return (
        json.dumps(pruned_fig, cls=plotly.utils.PlotlyJSONEncoder),
        json.dumps(unpruned_fig, cls=plotly.utils.PlotlyJSONEncoder),
    )


if __name__ == "__main__":
    main()
