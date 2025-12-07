from app.db import get_db
from app.models import Combo, Dish

__all__ = [
    "add_combo",
    "get_combos",
    "get_combo_by_id",
    "update_combo_by_id",
    "delete_combo_by_id",
    "add_dish_to_combo",
    "remove_dish_from_combo",
    "get_dishes_in_combo",
]


def add_combo(data: dict):
    """
    新增套餐

    :param data: 套餐資料字典

    :return: 新增的套餐資料或 None
    """
    db = get_db()

    combo = Combo.model_validate(data)

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO combo (name, image_url, price)
                VALUES (%s, %s, %s);
                """,
                (combo.name, combo.image_url, combo.price),
            )

        db.commit()

        combo_id = cursor.lastrowid
    except Exception as e:
        print(f"Error adding combo: {e}")
        db.rollback()
        return None

    return get_combo_by_id(combo_id)


def get_combos(keyword: str = ""):
    """
    取得所有套餐

    :param keyword: 搜尋關鍵字

    :return: 套餐列表
    """

    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM combo WHERE name LIKE %s;
                """,
                (f"%{keyword}%",),
            )

        rows = cursor.fetchall()
    except Exception as e:
        print(f"Error getting combos: {e}")
        return []

    combos = [Combo.model_validate(row) for row in rows]

    return combos


def get_combo_by_id(combo_id: int):
    """
    取得指定 ID 的套餐

    :param combo_id: 套餐 ID

    :return: 套餐資料或 None
    """
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM combo WHERE id = %s;
                """,
                (combo_id,),
            )

        row = cursor.fetchone()

        if not row:
            return None
    except Exception as e:
        print(f"Error getting combo by id: {e}")
        return None

    combo = Combo.model_validate(row)
    dishes = get_dishes_in_combo(combo)
    combo.dishes = dishes

    return combo


def update_combo_by_id(combo_id: int, data: dict):
    """
    更新指定 ID 的套餐

    :param combo_id: 套餐 ID
    :param data: 更新後的套餐資料字典

    :return: 更新後的套餐資料或 None
    """
    db = get_db()

    combo = Combo.model_validate(data)

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                UPDATE combo
                SET name = %s, image_url = %s, price = %s
                WHERE id = %s;
                """,
                (
                    combo.name,
                    combo.image_url,
                    combo.price,
                    combo_id,
                ),
            )

        db.commit()
    except Exception as e:
        print(f"Error updating combo by id: {e}")
        db.rollback()
        return None

    return get_combo_by_id(combo_id)


def delete_combo_by_id(combo_id: int):
    """
    刪除指定 ID 的套餐

    :param combo_id: 套餐 ID

    :return: 是否刪除成功
    """
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM combo WHERE id = %s;
                """,
                (combo_id,),
            )

        db.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error deleting combo by id: {e}")
        db.rollback()
        return False


# ====================
# Combo Dishes
# ====================


def add_dish_to_combo(combo: Combo, dish: Dish):
    """
    將菜品加入套餐

    :param combo: 套餐資料
    :param dish: 菜品資料

    :return: 是否加入成功
    """
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO combo_dish (combo_id, dish_id)
                VALUES (%s, %s);
                """,
                (combo.id, dish.id),
            )

        db.commit()
    except Exception as e:
        print(f"Error adding dish to combo: {e}")
        db.rollback()
        return False

    combo.dishes.append(dish)

    return True


def remove_dish_from_combo(combo: Combo, dish: Dish):
    """
    從套餐中移除菜品

    :param combo: 套餐資料
    :param dish: 菜品資料

    :return: 是否移除成功
    """
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM combo_dish
                WHERE combo_id = %s AND dish_id = %s;
                """,
                (combo.id, dish.id),
            )

        db.commit()

        # 沒有刪除任何資料，表示菜品不在套餐中
        if cursor.rowcount == 0:
            return False
    except Exception as e:
        print(f"Error removing dish from combo: {e}")
        db.rollback()
        return False

    combo.dishes.remove(dish)

    return True


def get_dishes_in_combo(combo: Combo):
    """
    取得套餐中的所有菜品

    :param combo: 套餐資料
    :return: 菜品列表
    """
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                SELECT d.*
                FROM dish d
                JOIN combo_dish cd ON d.id = cd.dish_id
                WHERE cd.combo_id = %s;
                """,
                (combo.id,),
            )

        rows = cursor.fetchall()
    except Exception as e:
        print(f"Error getting dishes in combo: {e}")
        return []

    dishes = [Dish.model_validate(row) for row in rows]

    return dishes
