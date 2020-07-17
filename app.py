from sqlalchemy import func
import pandas as pd
# from sqlalchemy import create_engine
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")

    @app.route("/predict")
def ml_app():
    return render_template("ml.html")

@app.route("/respitory_diseases")
def respitory():
    return render_template("index.html")

@app.route("/external_causes")
def external():
    return render_template("index.html")

@app.route("/nervous_system")
def nervous():
    return render_template("index.html")

@app.route("/metabolic_disorders")
def endocrine():
    return render_template("index.html")

@app.route("/mental_disorders")
def mental():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
