import json
import pickle

import dotenv
from flask import Flask, render_template
import plotly

from graph import GramGraph, test_data

dotenv.load_dotenv()

app = Flask(__name__)

with open("followers.pickle", "rb") as f:
    followers = pickle.load(f)

# G = GramGraph(test_data)
G = GramGraph(followers)
figure = G.plot_graph()
figure_JSON = json.dumps(figure, cls=plotly.utils.PlotlyJSONEncoder)


@app.route("/")
def index():
    return render_template(
        "base.html", figure_JSON=figure_JSON, main_account="happyhoundsza"
    )
