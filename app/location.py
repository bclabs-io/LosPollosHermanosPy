from flask import Blueprint, render_template

location_bp = Blueprint("location", __name__)


@location_bp.route("/location")
def location():
    return render_template("location.html")
