from app.db import get_db
from app.models import Dish, Ingredient, Supplier

__all__ = [
    "add_ingredient",
    "get_ingredients",
    "count_ingredients",
    "get_ingredient_by_id",
    "get_ingredient_by_name",
    "update_ingredient_by_id",
    "delete_ingredient_by_id",
    "get_suppliers_by_ingredient",
    "get_dishes_by_ingredient",
]


def add_ingredient(data: dict):
    """
    新增食材

    :param data: 食材資料字典

    :return: 新增的食材資料或 None
    """
    db = get_db()

    ingredient = Ingredient.model_validate(data)

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO ingredient (name)
                VALUES (%s);
                """,
                (ingredient.name,),
            )
            db.commit()
            ingredient_id = cursor.lastrowid
    except Exception as e:
        print("Error adding ingredient:", e)
        db.rollback()
        return None

    return get_ingredient_by_id(ingredient_id)


def count_ingredients(keyword: str = ""):
    """
    計算食材總數

    :param keyword: 搜尋關鍵字

    :return: 食材總數
    """
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                SELECT COUNT(*) AS total FROM ingredient
                WHERE name LIKE %s;
                """,
                (f"%{keyword}%",),
            )
            row = cursor.fetchone()
    except Exception as e:
        print("Error counting ingredients:", e)
        return 0

    total = row["total"] if row else 0

    return total


def get_ingredients(keyword: str = "", offset: int = 0, limit: int = 100):
    """
    取得食材列表

    :param keyword: 搜尋關鍵字

    :return: 食材列表
    """
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM ingredient
                WHERE name LIKE %s
                LIMIT %s OFFSET %s;
                """,
                (f"%{keyword}%", limit, offset),
            )
            rows = cursor.fetchall()
    except Exception as e:
        print("Error fetching ingredients:", e)
        return []

    ingredients = [Ingredient.model_validate(row) for row in rows]

    return ingredients


def get_ingredient_by_id(ingredient_id: int):
    """
    透過 ID 取得食材資料

    :param ingredient_id: 食材 ID

    :return: 食材資料或 None
    """
    db = get_db()
    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM ingredient WHERE id = %s;
                """,
                (ingredient_id,),
            )
            row = cursor.fetchone()
    except Exception as e:
        print("Error fetching ingredient by id:", e)
        return None

    if row is None:
        return None

    ingredient = Ingredient.model_validate(row)
    return ingredient


def get_ingredient_by_name(ingredient_name: str):
    """
    透過名稱取得食材資料

    :param ingredient_name: 食材名稱

    :return: 食材資料或 None
    """
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM ingredient WHERE name = %s;
                """,
                (ingredient_name,),
            )
            row = cursor.fetchone()
    except Exception as e:
        print("Error fetching ingredient by name:", e)
        return None

    if row is None:
        return None

    ingredient = Ingredient.model_validate(row)
    return ingredient


def update_ingredient_by_id(ingredient_id: int, data: dict):
    """
    更新食材資料

    :param ingredient_id: 食材 ID
    :param data: 更新後的食材資料字典

    :return: 更新後的食材資料或 None
    """
    db = get_db()
    ingredient = Ingredient.model_validate(data)

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                UPDATE ingredient
                SET name = %s
                WHERE id = %s;
                """,
                (ingredient.name, ingredient_id),
            )
            db.commit()
    except Exception as e:
        print("Error updating ingredient:", e)
        db.rollback()
        return None

    return get_ingredient_by_id(ingredient_id)


def delete_ingredient_by_id(ingredient_id: int):
    """
    刪除食材

    :param ingredient_id: 食材 ID

    :return: 是否刪除成功
    """
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM ingredient WHERE id = %s;
                """,
                (ingredient_id,),
            )
            db.commit()
            return cursor.rowcount > 0
    except Exception as e:
        print("Error deleting ingredient:", e)
        db.rollback()
        return False


# ====================
# Ingredient from Suppliers
# ====================


def get_suppliers_by_ingredient(ingredient: Ingredient):
    """
    透過食材取得供應商列表

    :param ingredient: 食材資料

    :return: 供應商列表
    """
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                SELECT s.* FROM supplier s
                JOIN supplier_ingredient si ON s.id = si.supplier_id
                WHERE si.ingredient_id = %s;
                """,
                (ingredient.id,),
            )
            rows = cursor.fetchall()
    except Exception as e:
        print("Error fetching suppliers by ingredient:", e)
        return []

    suppliers = [Supplier.model_validate(row) for row in rows]

    return suppliers


# ====================
# Ingredients in Dishes
# ====================


def get_dishes_by_ingredient(ingredient: Ingredient):
    """
    透過食材取得使用該食材的菜餚列表

    :param ingredient: 食材資料

    :return: 菜餚列表
    """
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                SELECT d.* FROM dish d
                JOIN dish_ingredient di ON d.id = di.dish_id
                WHERE di.ingredient_id = %s;
                """,
                (ingredient.id,),
            )
            rows = cursor.fetchall()
    except Exception as e:
        print("Error fetching dishes by ingredient:", e)
        return []

    dishes = [Dish.model_validate(row) for row in rows]

    return dishes
