from flask import Blueprint, abort, render_template, request, url_for

from app.services import add_dish, delete_dish_by_id, get_dish_by_id, update_dish_by_id

dish_bp = Blueprint("dish", __name__, url_prefix="/menu/dishes")


@dish_bp.route("/<int:dish_id>")
def view_dish(dish_id):
    data = get_dish_by_id(dish_id)

    if data is None:
        abort(404)

    return render_template("dish/detail.html", dish=data)


@dish_bp.route("/add", methods=["GET", "POST"])
def add_dish_view():
    if request.method == "POST":
        # 處理新增餐點的表單提交
        form = request.form
        data = {
            "name": form.get("name"),
            "description": form.get("description"),
            "calories": form.get("calories"),
            "price": form.get("price"),
            "image": request.files.get("image"),
        }

        # 處理配料資訊
        ingredient_names = form.getlist("ingredients[]name")
        ingredient_quantities = form.getlist("ingredients[]quantity")
        ingredient_units = form.getlist("ingredients[]unit")

        data["ingredients"] = [
            {"name": name, "quantity": float(quantity), "unit": unit}
            for name, quantity, unit in zip(ingredient_names, ingredient_quantities, ingredient_units)
        ]

        dish = add_dish(data)
        redirect_url = url_for("dish.view_dish", dish_id=dish.id)
        return render_template("saved.html", item_name=dish.name, url=redirect_url)

    ########################################

    return render_template("dish/add.html")


@dish_bp.route("/<int:dish_id>/edit", methods=["GET", "POST"])
def edit_dish(dish_id):
    dish = get_dish_by_id(dish_id)

    if dish is None:
        abort(404)

    ########################################

    if request.method == "POST":
        # 儲存修改後的餐點資訊
        form = request.form
        data = {
            "name": form.get("name"),
            "description": form.get("description"),
            "calories": form.get("calories"),
            "price": form.get("price"),
            "image": request.files.get("image"),
        }

        # 處理配料資訊
        ingredient_names = form.getlist("ingredients[]name")
        ingredient_quantities = form.getlist("ingredients[]quantity")
        ingredient_units = form.getlist("ingredients[]unit")

        data["ingredients"] = [
            {"name": name, "quantity": float(quantity), "unit": unit}
            for name, quantity, unit in zip(ingredient_names, ingredient_quantities, ingredient_units)
        ]

        dish = update_dish_by_id(dish_id, data)
        redirect_url = url_for("dish.view_dish", dish_id=dish_id)
        return render_template("saved.html", item_name=dish.name, url=redirect_url)

    ########################################

    return render_template("dish/edit.html", dish=dish)


@dish_bp.route("/<int:dish_id>/delete")
def delete_dish(dish_id):
    dish = get_dish_by_id(dish_id)

    if dish is None:
        abort(404)

    delete_dish_by_id(dish_id)
    redirect_url = url_for("menu.menu")
    return render_template("delete-item.html", item_name=dish.name, url=redirect_url)
