from flask import Blueprint, abort, render_template, request

from app.services import get_dishes_by_ingredient, get_ingredient_by_id, get_ingredients, get_suppliers_by_ingredient

ingredient_bp = Blueprint("ingredient", __name__, url_prefix="/ingredients")


@ingredient_bp.route("/")
def ingredients():
    """
    食材列表頁面
    """
    keyword = request.args.get("query", "")
    ingredients = get_ingredients(keyword=keyword)

    return render_template("ingredient/list.html", ingredients=ingredients, keyword=keyword)


@ingredient_bp.route("/<int:ingredient_id>")
def view_ingredient(ingredient_id: int):
    """
    食材詳細頁面
    """
    ingredient = get_ingredient_by_id(ingredient_id)

    if ingredient is None:
        abort(404)

    suppliers = get_suppliers_by_ingredient(ingredient)
    dishes = get_dishes_by_ingredient(ingredient)

    deletable = len(dishes) == 0 and len(suppliers) == 0

    return render_template(
        "ingredient/detail.html",
        ingredient=ingredient,
        suppliers=suppliers,
        dishes=dishes,
        deletable=deletable,
    )
