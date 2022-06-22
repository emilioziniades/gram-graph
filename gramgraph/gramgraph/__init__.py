from pathlib import Path

from flask import Flask, render_template, request

# from .data import collect_data
from .graph import save_figures_JSON
from .config import DATA_DIRECTORY


app = Flask(__name__)

# hard coded for now
USER = "happyhoundsza"


@app.route("/")
def index() -> str:
    pruned_JSON = Path(f"{DATA_DIRECTORY}/pruned_figure.json").read_text()
    unpruned_JSON = Path(f"{DATA_DIRECTORY}/unpruned_figure.json").read_text()
    prune = bool(request.args.get("prune", False))
    return render_template(
        "base.html",
        figure_JSON=pruned_JSON if prune else unpruned_JSON,
        main_account=USER,
        prune=prune,
    )


@app.cli.command("prepare")
def prepare_graphs(user: str = USER) -> None:
    print("preparing graphs")
    save_figures_JSON(user)


# @app.cli.command("collect")
# def collect_graph_data():
#     collect_data()
