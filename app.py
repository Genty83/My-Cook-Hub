""" Main app file: This file is the entry point to the application """

import os
from src import app
from flask import render_template


# Landing page
@app.route("/")
def home():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(
        host = os.environ.get("IP"),
        port = int(os.environ.get("PORT")),
        debug = os.environ.get("DEBUG")
    )