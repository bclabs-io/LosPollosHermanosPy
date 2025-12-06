from dotenv import load_dotenv
from flask import Flask, abort, render_template

from app.errors import error_bp

load_dotenv()

app = Flask(__name__)
app.register_blueprint(error_bp)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    abort(418)


if __name__ == "__main__":
    app.run(debug=True)
