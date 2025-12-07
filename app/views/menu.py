from flask import Blueprint, abort, redirect, render_template, request, url_for

from app.services import (
    delete_combo_by_id,
    delete_dish_by_id,
    get_combo_by_id,
    get_combos,
    get_dish_by_id,
    get_dishes,
    get_suppliers,
)

menu_bp = Blueprint("menu", __name__, url_prefix="/menu")


@menu_bp.route("/")
def menu():
    dishes = get_dishes()
    combos = get_combos()

    return render_template("menu/menu.html", dishes=dishes, combos=combos)


@menu_bp.route("/dish/<int:dish_id>/edit", methods=["GET", "POST"])
def edit_dish(dish_id):
    if request.method == "POST":
        # 儲存修改後的菜品資訊
        # Handle form submission to update dish details
        form = request.form.to_dict()

        print(form)
        return redirect(url_for("menu.menu"))

    # 顯示編輯表單
    data = get_dish_by_id(dish_id)
    suppliers = get_suppliers()

    if data is None:
        abort(404)

    return render_template("menu/edit-dish.html", data=data, suppliers=suppliers)


@menu_bp.route("/dish/<int:dish_id>/delete")
def delete_dish(dish_id):
    dish = get_dish_by_id(dish_id)

    if dish is None:
        abort(404)

    delete_dish_by_id(dish_id)

    return render_template("delete-item.html", item_name=dish.name, url=url_for("menu.menu"))

