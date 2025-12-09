from app.db import get_db
from app.models import Combo, Dish

from .dish import get_dish_by_name
from .image import process_image_upload

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

    after = data.pop("dishes", [])
    data = process_image_upload(data)

    # 驗證資料
    combo = Combo.model_validate(data)

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO combo (name, description, price, image_url)
                VALUES (%s, %s, %s, %s);
                """,
                (combo.name, combo.description, combo.price, combo.image_url),
            )
            db.commit()
            combo_id = cursor.lastrowid
    except Exception as e:
        print(f"Error adding combo: {e}")
        db.rollback()
        return None

    # 處理餐點關聯
    combo = get_combo_by_id(combo_id)
    update_combo_dishes(combo, before=[], after=after)

    return combo


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
    get_dishes_in_combo(combo)

    return combo


def update_combo_by_id(combo_id: int, data: dict):
    """
    更新指定 ID 的套餐

    :param combo_id: 套餐 ID
    :param data: 更新後的套餐資料字典

    :return: 更新後的套餐資料或 None
    """
    db = get_db()

    original_combo = get_combo_by_id(combo_id)
    if not original_combo:
        return None

    before = [dish.name for dish in original_combo.dishes]
    after = set(data.pop("dishes", []))
    data = process_image_upload(data, original_combo.image_url)

    # 驗證資料
    combo = Combo.model_validate(data)

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                UPDATE combo
                SET name = %s, description = %s, price = %s, image_url = %s
                WHERE id = %s;
                """,
                (
                    combo.name,
                    combo.description,
                    combo.price,
                    combo.image_url,
                    combo_id,
                ),
            )
            db.commit()
    except Exception as e:
        print(f"Error updating combo by id: {e}")
        db.rollback()
        return None

    # 處理餐點關聯
    combo = get_combo_by_id(combo_id)
    update_combo_dishes(combo, before=before, after=after)

    return combo


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
    將餐點加入套餐

    :param combo: 套餐資料
    :param dish: 餐點資料

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
    從套餐中移除餐點

    :param combo: 套餐資料
    :param dish: 餐點資料

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
            # 沒有刪除任何資料，表示餐點不在套餐中
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Error removing dish from combo: {e}")
        db.rollback()
        return False

    combo.dishes.remove(dish)

    return True


def update_combo_dishes(combo: Combo, before: list[str], after: list[str]):
    """
    更新套餐中的餐點列表

    :param combo: 套餐資料
    :param before: 更新前的餐點名稱列表
    :param after: 更新後的餐點名稱列表

    :return: 是否更新成功
    """
    before = set(before)
    after = set(after)
    to_adds = after - before
    to_removes = before - after

    # 添加新的餐點
    for dish_name in to_adds:
        dish = get_dish_by_name(dish_name)
        if not dish:
            print(f"Dish '{dish_name}' not found. Skipping addition to combo.")
            continue
        add_dish_to_combo(combo, dish)

    # 移除不需要的餐點
    for dish_name in to_removes:
        dish = get_dish_by_name(dish_name)
        if not dish:
            print(f"Dish '{dish_name}' not found. Skipping removal from combo.")
            continue
        remove_dish_from_combo(combo, dish)


def get_dishes_in_combo(combo: Combo):
    """
    取得套餐中的所有餐點

    :param combo: 套餐資料

    :return: 套餐資料，包含餐點列表及總熱量
    """
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                SELECT d.* FROM dish d
                JOIN combo_dish cd ON d.id = cd.dish_id
                WHERE cd.combo_id = %s;
                """,
                (combo.id,),
            )
            rows = cursor.fetchall()

            cursor.execute(
                """
                SELECT SUM(calories) AS total_calories FROM dish d
                JOIN combo_dish cd ON d.id = cd.dish_id
                WHERE cd.combo_id = %s;
                """,
                (combo.id,),
            )
            total_calries = cursor.fetchone()
    except Exception as e:
        print(f"Error getting dishes in combo: {e}")
        return []

    dishes = [Dish.model_validate(row) for row in rows]
    combo.dishes = dishes
    combo.total_calories = total_calries["total_calories"] if total_calries else 0

    return dishes
