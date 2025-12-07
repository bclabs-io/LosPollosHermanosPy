from flask import Flask, abort, render_template

from .views import register

app = Flask(__name__, static_folder="../static", template_folder="../templates")
register(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    abort(418)


def create_app():
    return app
