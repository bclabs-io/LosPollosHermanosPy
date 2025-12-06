from flask import Flask, abort, render_template

from .db import create_tables, drop_all_tables, get_db_connection  # noqa: F401
from .errors import error_bp
from .location import location_bp
from .menu import menu_bp

app = Flask(__name__, static_folder="../static", template_folder="../templates")
app.register_blueprint(error_bp)
app.register_blueprint(location_bp)
app.register_blueprint(menu_bp)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    abort(418)


def create_app():
    return app
