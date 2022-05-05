import json

import dotenv
from flask import Flask, render_template
import plotly

from graph import GramGraph, test_data

dotenv.load_dotenv()

app = Flask(__name__)


@app.route("/")
def index():
    G = GramGraph(test_data)
    figure = G.plot_graph()
    figure_JSON = json.dumps(figure, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("base.html", figure_JSON=figure_JSON)
