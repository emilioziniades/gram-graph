import dotenv
from flask import Flask

dotenv.load_dotenv()

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<h1>Hello world</h1>"
