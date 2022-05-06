from pathlib import Path
from flask import Flask, render_template, request


app = Flask(__name__)

pruned_JSON = Path("data/pruned_figure.json").read_text()
unpruned_JSON = Path("data/unpruned_figure.json").read_text()


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
