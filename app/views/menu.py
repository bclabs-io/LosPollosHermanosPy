from flask import Blueprint, render_template

from app.services import get_combos, get_dishes

menu_bp = Blueprint("menu", __name__, url_prefix="/menu")


@menu_bp.route("/")
def menu():
    dishes = get_dishes()
    combos = get_combos()

    return render_template("menu/menu.html", dishes=dishes, combos=combos)
