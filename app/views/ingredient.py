from flask import Blueprint, abort, render_template, request, url_for

from app.services import (
    count_ingredients,
    delete_ingredient_by_id,
    get_dishes_by_ingredient,
    get_ingredient_by_id,
    get_ingredients,
    get_suppliers_by_ingredient,
)

ingredient_bp = Blueprint("ingredient", __name__, url_prefix="/ingredients")


@ingredient_bp.route("/")
def ingredients():
    """
    食材列表頁面
    """
    keyword = request.args.get("query", "")
    total = count_ingredients(keyword=keyword)
    page = request.args.get("page", 1, type=int)
    per_page = 20
    offset = (page - 1) * per_page
    ingredients = get_ingredients(keyword=keyword, offset=offset, limit=per_page)

    return render_template("ingredient/list.html", ingredients=ingredients, keyword=keyword, total=total, page=page)


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


@ingredient_bp.route("/<int:ingredient_id>/delete")
def delete_ingredient(ingredient_id: int):
    """
    刪除食材
    """
    ingredient = get_ingredient_by_id(ingredient_id)

    if ingredient is None:
        abort(404)

    suppliers = get_suppliers_by_ingredient(ingredient)
    dishes = get_dishes_by_ingredient(ingredient)

    if len(dishes) > 0 or len(suppliers) > 0:
        abort(400, description="Cannot delete ingredient that is in use.")

    delete_ingredient_by_id(ingredient_id)

    redirect_url = url_for("ingredient.ingredients")
    return render_template("delete-item.html", item_name=ingredient.name, url=redirect_url)
