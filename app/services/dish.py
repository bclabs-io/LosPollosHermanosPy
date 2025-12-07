from app.db import get_db
from app.models import Dish, Ingredient, IngredientInDish

__all__ = [
    "add_dish",
    "get_dishes",
    "get_dish_by_id",
    "update_dish_by_id",
    "delete_dish_by_id",
    "add_ingredient_to_dish",
    "remove_ingredient_from_dish",
    "get_ingredients_in_dish",
]


def add_dish(data: dict):
    """
    新增單點菜品

    :param data: 菜品資料字典

    :return: 新增的菜品資料或 None
    """
    db = get_db()
    dish = Dish.model_validate(data)

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO dish (name, calories, price, image_url)
                VALUES (%s, %s, %s, %s);
                """,
                (dish.name, dish.calories, dish.price, dish.image_url),
            )

        db.commit()
        dish_id = cursor.lastrowid
    except Exception as e:
        print(f"Error adding dish: {e}")
        db.rollback()
        return None

    return get_dish_by_id(dish_id)


def get_dishes(keyword: str = ""):
    """
    取得所有單點菜品

    :param keyword: 搜尋關鍵字

    :return: 菜品列表
    """
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM dish WHERE name LIKE %s;
                """,
                (f"%{keyword}%",),
            )

        rows = cursor.fetchall()
    except Exception as e:
        print(f"Error getting dishes: {e}")
        return None

    dishes = [Dish.model_validate(row) for row in rows]

    return dishes


def get_dish_by_id(dish_id: int):
    """
    取得指定 ID 的單點菜品

    :param dish_id: 菜品 ID

    :return: 菜品資料或 None
    """
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM dish WHERE id = %s;
                """,
                (dish_id,),
            )

        row = cursor.fetchone()

        if not row:
            return None
    except Exception as e:
        print(f"Error getting dish by id: {e}")
        return None

    dish = Dish.model_validate(row)
    ingredients = get_ingredients_in_dish(dish)
    dish.ingredients = ingredients

    return dish


def update_dish_by_id(dish_id: int, data: dict):
    """
    更新指定 ID 的單點菜品

    :param dish_id: 菜品 ID
    :param data: 更新後的菜品資料字典
    """
    db = get_db()

    dish = Dish.model_validate(data)

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                UPDATE dish
                SET name = %s, image_url = %s, calories = %s, price = %s
                WHERE id = %s;
                """,
                (
                    dish.name,
                    dish.image_url,
                    dish.calories,
                    dish.price,
                    dish_id,
                ),
            )

        db.commit()
    except Exception as e:
        print(f"Error updating dish by id: {e}")
        db.rollback()
        return None

    return get_dish_by_id(dish_id)


def delete_dish_by_id(dish_id: int):
    """
    刪除指定 ID 的單點菜品

    :param dish_id: 菜品 ID

    :return: 是否刪除成功
    """
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM dish WHERE id = %s;
                """,
                (dish_id,),
            )

        db.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error deleting dish by id: {e}")
        db.rollback()
        return False


# ====================
# Dish Ingredients
# ====================


def add_ingredient_to_dish(dish: Dish, ingredient: Ingredient, quantity: float, unit: str):
    """
    為菜品新增食材

    :param dish: 菜品資料
    :param ingredient: 食材資料
    :param quantity: 食材數量
    :param unit: 食材單位

    :return: 是否新增成功
    """
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO dish_ingredient (dish_id, ingredient_id, quantity, unit)
                VALUES (%s, %s, %s, %s);
                """,
                (dish.id, ingredient.id, quantity, unit),
            )

        db.commit()
    except Exception as e:
        print(f"Error adding ingredient to dish: {e}")
        db.rollback()
        return False

    return True


def remove_ingredient_from_dish(dish: Dish, ingredient: Ingredient):
    """
    從菜品移除食材

    :param dish: 菜品資料
    :param ingredient: 食材資料

    :return: 是否移除成功
    """
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM dish_ingredient
                WHERE dish_id = %s AND ingredient_id = %s;
                """,
                (dish.id, ingredient.id),
            )

        db.commit()

        # 沒有刪除任何資料，表示食材不在菜品中
        if cursor.rowcount == 0:
            return False
    except Exception as e:
        print(f"Error removing ingredient from dish: {e}")
        db.rollback()
        return False

    return True


def get_ingredients_in_dish(dish: Dish):
    """
    取得菜品中的所有食材

    :param dish: 菜品資料

    :return: 食材列表
    """
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                SELECT i.*, di.quantity, di.unit
                FROM ingredient i
                JOIN dish_ingredient di ON i.id = di.ingredient_id
                WHERE di.dish_id = %s;
                """,
                (dish.id,),
            )

        rows = cursor.fetchall()
    except Exception as e:
        print(f"Error getting ingredients in dish: {e}")
        return []

    ingredients = [IngredientInDish.model_validate(row) for row in rows]

    return ingredients
