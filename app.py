import json
import pickle
from typing import Tuple

from flask import Flask, render_template, request
import plotly

from graph import GramGraph, test_data

app = Flask(__name__)


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


pruned_JSON, unpruned_JSON = get_figures_JSON()


@app.route("/")
def index():
    print(request.args)
    prune = bool(request.args.get("prune", False))
    return render_template(
        "base.html",
        figure_JSON=pruned_JSON if prune else unpruned_JSON,
        main_account="happyhoundsza",
        prune=prune,
    )
