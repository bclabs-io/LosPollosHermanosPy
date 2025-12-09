from flask import Blueprint, abort, render_template, request, url_for

from app.services import add_combo, delete_combo_by_id, get_combo_by_id, get_dishes, update_combo_by_id

combo_bp = Blueprint("combo", __name__, url_prefix="/menu/combos")


@combo_bp.route("/<int:combo_id>")
def view_combo(combo_id):
    combo = get_combo_by_id(combo_id)

    if combo is None:
        abort(404)

    return render_template("combo/detail.html", combo=combo)


@combo_bp.route("/add", methods=["GET", "POST"])
def add_combo_view():
    if request.method == "POST":
        form = request.form

        data = {
            "name": form.get("name", ""),
            "price": float(form.get("price", 0)),
            "description": form.get("description", ""),
            "image": request.files.get("image"),
            "dishes": form.getlist("dishes[]"),
        }

        combo = add_combo(data)

        redirect_url = url_for("combo.view_combo", combo_id=combo.id)
        return render_template("saved.html", item_name=combo.name, url=redirect_url)

    ########################################

    all_dishes = get_dishes()
    return render_template("combo/add.html", all_dishes=all_dishes)


@combo_bp.route("/<int:combo_id>/edit", methods=["GET", "POST"])
def edit_combo(combo_id):
    combo = get_combo_by_id(combo_id)

    if combo is None:
        abort(404)

    ########################################

    if request.method == "POST":
        form = request.form

        data = {
            "name": form.get("name", ""),
            "price": float(form.get("price", 0)),
            "description": form.get("description", ""),
            "dishes": form.getlist("dishes[]"),
            "image": request.files.get("image"),
        }

        combo = update_combo_by_id(combo_id, data)

        redirect_url = url_for("combo.view_combo", combo_id=combo.id)
        return render_template("saved.html", item_name=combo.name, url=redirect_url)

    ########################################

    all_dishes = get_dishes()

    return render_template("combo/edit.html", combo=combo, all_dishes=all_dishes)


@combo_bp.route("/<int:combo_id>/delete")
def delete_combo(combo_id):
    combo = get_combo_by_id(combo_id)

    if combo is None:
        abort(404)

    delete_combo_by_id(combo_id)

    redirect_url = url_for("menu.menu")
    return render_template("delete-item.html", item_name=combo.name, url=redirect_url)
