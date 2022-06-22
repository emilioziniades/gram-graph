import json
from pathlib import Path

from flask import Flask, render_template, request

from .data import collect_data
from .graph import save_figures_JSON
from .config import (
    DATA_DIRECTORY,
    PRUNED_FIGURE_FILENAME,
    UNPRUNED_FIGURE_FILENAME,
    SUMMARY_DATA_FILENAME,
    ACCOUNT,
)


app = Flask(__name__)


@app.route("/")
def index() -> str:
    PRUNE = True
    if PRUNE:
        figure_JSON = Path(DATA_DIRECTORY, PRUNED_FIGURE_FILENAME).read_text()
    else:
        figure_JSON = Path(DATA_DIRECTORY, UNPRUNED_FIGURE_FILENAME).read_text()

    most_followed_JSON = Path(DATA_DIRECTORY, SUMMARY_DATA_FILENAME).read_text()
    most_followed = json.loads(most_followed_JSON)

    return render_template(
        "base.html",
        figure_JSON=figure_JSON,
        most_followed=most_followed,
        main_account=ACCOUNT,
    )


@app.cli.command("prepare")
def prepare_graph(user: str = ACCOUNT, prune: bool = True) -> None:
    print("preparing graphs")
    save_figures_JSON(user, prune)


@app.cli.command("collect")
def collect_graph_data():
    collect_data()
