from app.db import get_db
from app.models import Ingredient, Supplier, SupplierSummary

from .image import process_image_upload
from .ingredient import add_ingredient, get_ingredient_by_name

__all__ = [
    "add_supplier",
    "get_suppliers",
    "get_supplier_by_id",
    "update_supplier_by_id",
    "delete_supplier_by_id",
    "add_ingredient_to_supplier",
    "remove_ingredient_from_supplier",
    "get_ingredients_by_supplier",
]


def add_supplier(data: dict):
    """
    新增供應商

    :param supplier: 供應商資料字典

    :return: 新增的供應商資料
    """
    db = get_db()

    # 處理需要關聯的食材列表
    after = data.get("ingredients", [])
    data = process_image_upload(data)

    # 驗證資料
    supplier = Supplier.model_validate(data)

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO supplier (name, description, contact_person, email, phone,
                    state, city, address, image_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
                """,
                (
                    supplier.name,
                    supplier.description,
                    supplier.contact_person,
                    supplier.email,
                    supplier.phone,
                    supplier.state,
                    supplier.city,
                    supplier.address,
                    supplier.image_url,
                ),
            )
            db.commit()
            supplier_id = cursor.lastrowid
    except Exception as e:
        print("Error adding supplier:", e)
        db.rollback()
        return None

    # 處理食材關聯
    supplier = get_supplier_by_id(supplier_id)
    update_supplier_ingredients(supplier, before=[], after=after)

    return supplier


def get_suppliers(keyword: str = ""):
    """
    取得供應商列表

    :param keyword: 搜尋關鍵字

    :return: 供應商列表
    """
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, name, description, image_url FROM supplier
                WHERE name LIKE %s;
                """,
                (f"%{keyword}%",),
            )
            rows = cursor.fetchall()
    except Exception as e:
        print("Error fetching suppliers:", e)
        return []

    suppliers = [SupplierSummary.model_validate(row) for row in rows]

    return suppliers


def get_supplier_by_id(supplier_id: int):
    """
    根據 ID 取得供應商資訊

    :param supplier_id: 供應商 ID

    :return: 供應商資料或 None
    """
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM supplier WHERE id = %s;
                """,
                (supplier_id,),
            )
            row = cursor.fetchone()
    except Exception as e:
        print("Error fetching supplier by id:", e)
        return None

    if row is None:
        return None

    supplier = Supplier.model_validate(row)
    ingredients = get_ingredients_by_supplier(supplier)
    supplier.ingredients = ingredients

    return supplier


def update_supplier_by_id(supplier_id: int, data: dict):
    """
    更新供應商資訊

    :param supplier_id: 供應商 ID
    :param data: 更新後的供應商資料字典

    :return: 更新後的供應商資料
    """
    db = get_db()

    original_supplier = get_supplier_by_id(supplier_id)
    if original_supplier is None:
        return None

    before = [ing.name for ing in original_supplier.ingredients]
    after = data.pop("ingredients", [])
    data = process_image_upload(data, original_supplier.image_url)

    # 驗證資料
    supplier = Supplier.model_validate(data)

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                UPDATE supplier
                SET name = %s, description = %s, contact_person = %s, email = %s, phone = %s,
                    state = %s, city = %s, address = %s, image_url = %s
                WHERE id = %s;
                """,
                (
                    supplier.name,
                    supplier.description,
                    supplier.contact_person,
                    supplier.email,
                    supplier.phone,
                    supplier.state,
                    supplier.city,
                    supplier.address,
                    supplier.image_url,
                    supplier_id,
                ),
            )
            db.commit()
    except Exception as e:
        print("Error updating supplier:", e)
        db.rollback()
        return None

    # 處理食材關聯
    supplier = get_supplier_by_id(supplier_id)
    update_supplier_ingredients(supplier, before=before, after=after)

    return supplier


def delete_supplier_by_id(supplier_id: int):
    """
    刪除供應商

    :param supplier_id: 供應商 ID

    :return: 是否刪除成功
    """
    db = get_db()
    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM supplier WHERE id = %s;
                """,
                (supplier_id,),
            )
            db.commit()
            return cursor.rowcount > 0
    except Exception as e:
        print("Error deleting supplier:", e)
        db.rollback()
        return False


# ====================
# Supplier Ingredients
# ====================


def add_ingredient_to_supplier(supplier: Supplier, ingredient: Ingredient):
    """
    為供應商新增食材

    :param supplier: 供應商資料
    :param ingredient: 食材資料

    :return: 是否新增成功
    """
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO supplier_ingredient (supplier_id, ingredient_id)
                VALUES (%s, %s);
                """,
                (supplier.id, ingredient.id),
            )
            db.commit()
    except Exception as e:
        print("Error adding ingredient to supplier:", e)
        db.rollback()
        return False

    return True


def remove_ingredient_from_supplier(supplier: Supplier, ingredient: Ingredient):
    """
    從供應商移除食材

    :param supplier: 供應商資料
    :param ingredient: 食材資料

    :return: 是否移除成功
    """
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM supplier_ingredient
                WHERE supplier_id = %s AND ingredient_id = %s;
                """,
                (supplier.id, ingredient.id),
            )
            db.commit()
            return cursor.rowcount > 0
    except Exception as e:
        print("Error removing ingredient from supplier:", e)
        db.rollback()
        return False


def update_supplier_ingredients(supplier: Supplier, before: list[str], after: list[str]):
    """
    更新供應商的食材列表

    :param supplier: 供應商資料
    :param before: 更新前的食材名稱列表
    :param after: 更新後的食材名稱列表
    """
    before = set(before)
    after = set(after)
    to_add = after - before
    to_remove = before - after

    # 添加新的食材
    for ing_name in to_add:
        ing = get_ingredient_by_name(ing_name)
        if not ing:
            ing = add_ingredient({"name": ing_name})
        add_ingredient_to_supplier(supplier, ing)

    # 移除不需要的食材
    for ing_name in to_remove:
        ing = get_ingredient_by_name(ing_name)
        remove_ingredient_from_supplier(supplier, ing)


def get_ingredients_by_supplier(supplier: Supplier):
    """
    根據供應商取得其供應的食材列表

    :param supplier: 供應商資料

    :return: 食材列表
    """
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                SELECT i.* FROM ingredient i
                JOIN supplier_ingredient si ON i.id = si.ingredient_id
                WHERE si.supplier_id = %s;
                """,
                (supplier.id,),
            )
            rows = cursor.fetchall()
    except Exception as e:
        print("Error fetching ingredients by supplier:", e)
        return []

    ingredients = [Ingredient.model_validate(row) for row in rows]

    return ingredients
