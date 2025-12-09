from datetime import time

from app.db import get_db
from app.models import Employee, Store

from .utils import timedelta_to_time

__all__ = [
    "add_store",
    "get_stores",
    "get_stores_nearby",
    "get_store_by_id",
    "get_store_by_name",
    "update_store_by_id",
    "delete_store_by_id",
    "count_employees_in_store",
    "get_employees_in_store",
]


def add_store(data: dict):
    """
    新增商店

    :param data: 商店資料字典

    :return: 新增的商店資料或 None
    """
    db = get_db()

    if len(data["open_time"]) == 5:
        data["open_time"] = f"{data['open_time']}:00"
    if len(data["close_time"]) == 5:
        data["close_time"] = f"{data['close_time']}:00"

    # 轉換時間格式
    data["open_time"] = time.fromisoformat(data["open_time"])
    data["close_time"] = time.fromisoformat(data["close_time"])

    # 驗證資料
    store = Store.model_validate(data)

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO store (name, phone, state, city, address, zipcode, latitude, longitude,
                    weekdays, open_time, close_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """,
                (
                    store.name,
                    store.phone,
                    store.state,
                    store.city,
                    store.address,
                    store.zipcode,
                    store.latitude,
                    store.longitude,
                    ",".join(map(str, store.weekdays)),
                    store.open_time,
                    store.close_time,
                ),
            )
            db.commit()
            store_id = cursor.lastrowid
    except Exception as e:
        print("Error adding store:", e)
        db.rollback()
        return None

    return get_store_by_id(store_id)


def get_stores(keyword: str = "", state: str = "", city: str = ""):
    """
    取得所有商店資料

    :param keyword: 搜尋關鍵字
    :param state: 州份名稱
    :param city: 城市名稱

    :return: 商店資料列表
    """
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM store WHERE name LIKE %s AND state LIKE %s AND city LIKE %s;
                """,
                (f"%{keyword}%", f"%{state}%", f"%{city}%"),
            )
            rows = cursor.fetchall()
    except Exception as e:
        print("Error fetching stores:", e)
        return []

    stores: list[Store] = []

    for row in rows:
        row["weekdays"] = list(map(int, row["weekdays"].split(",")))
        row["open_time"] = timedelta_to_time(row["open_time"])
        row["close_time"] = timedelta_to_time(row["close_time"])
        store = Store.model_validate(row)
        store.employees_count = count_employees_in_store(store.id)
        stores.append(store)

    return stores


def get_stores_nearby(latitude: float, longitude: float, radius_km: float = 5.0, keyword: str = ""):
    """
    根據經緯度取得附近的商店資料

    :param latitude: 緯度
    :param longitude: 經度
    :param radius_km: 半徑（公里）
    :param keyword: 搜尋關鍵字

    :return: 附近的商店資料列表
    """
    db = get_db()
    stores = []

    try:
        with db.cursor() as cursor:
            # 地球半徑約為 6371 公里
            cursor.execute(
                """
                SELECT *, (6371 * ACOS(
                                COS(RADIANS(%s))
                                * COS(RADIANS(latitude))
                                * COS(RADIANS(longitude) - RADIANS(%s))
                                + SIN(RADIANS(%s)) * SIN(RADIANS(latitude))
                            )) AS distance
                FROM store
                HAVING distance <= %s AND name LIKE %s
                ORDER BY distance;
                """,
                (latitude, longitude, latitude, radius_km, f"%{keyword}%"),
            )
            rows = cursor.fetchall()
    except Exception as e:
        print("Error fetching nearby stores:", e)
        return []

    stores = []

    for row in rows:
        row["weekdays"] = list(map(int, row["weekdays"].split(",")))
        row["open_time"] = timedelta_to_time(row["open_time"])
        row["close_time"] = timedelta_to_time(row["close_time"])
        store = Store.model_validate(row)
        store.employees_count = count_employees_in_store(store.id)
        stores.append(store)

    return stores


def get_store_by_id(store_id: int):
    """
    根據 ID 取得商店資訊

    :param store_id: 商店 ID

    :return: 商店資料或 None
    """
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM store WHERE id = %s;
                """,
                (store_id,),
            )
            row = cursor.fetchone()
    except Exception as e:
        print("Error fetching store by id:", e)
        return None

    if row is None:
        return None

    row["weekdays"] = list(map(int, row["weekdays"].split(",")))
    row["open_time"] = timedelta_to_time(row["open_time"])
    row["close_time"] = timedelta_to_time(row["close_time"])
    store = Store.model_validate(row)
    store.employees_count = count_employees_in_store(store.id)

    return store


def get_store_by_name(store_name: str):
    """
    根據名稱取得商店資訊

    :param store_name: 商店名稱

    :return: 商店資料或 None
    """
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM store WHERE name = %s;
                """,
                (store_name,),
            )
            row = cursor.fetchone()
    except Exception as e:
        print("Error fetching store by name:", e)
        return None

    if row is None:
        return None

    row["weekdays"] = list(map(int, row["weekdays"].split(",")))
    row["open_time"] = timedelta_to_time(row["open_time"])
    row["close_time"] = timedelta_to_time(row["close_time"])
    store = Store.model_validate(row)
    store.employees_count = count_employees_in_store(store.id)

    return store


def update_store_by_id(store_id: int, data: dict):
    """
    更新商店資料

    :param store_id: 商店 ID
    :param data: 要更新的商店資料字典

    :return: 更新後的商店資料或 None
    """
    db = get_db()

    if len(data["open_time"]) == 5:
        data["open_time"] = f"{data['open_time']}:00"
    if len(data["close_time"]) == 5:
        data["close_time"] = f"{data['close_time']}:00"

    # 轉換時間格式
    data["open_time"] = time.fromisoformat(data["open_time"])
    data["close_time"] = time.fromisoformat(data["close_time"])

    # 驗證資料
    store = Store.model_validate(data)

    # 生成更新語句
    fields = [f"{key}" for key in store.model_fields_set if key != "weekdays"]
    values = [getattr(store, key) for key in fields]
    fields.append("weekdays")
    values.append(",".join(map(str, store.weekdays)))
    values.append(store_id)

    try:
        with db.cursor() as cursor:
            cursor.execute(
                f"""
                UPDATE store SET {', '.join(fields)} WHERE id = %s;
                """,
                tuple(values),
            )
            db.commit()
    except Exception as e:
        print("Error updating store:", e)
        db.rollback()
        return None

    return get_store_by_id(store_id)


def delete_store_by_id(store_id: int):
    """
    刪除商店資料

    :param store_id: 商店 ID

    :return: 是否刪除成功
    """
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM store WHERE id = %s;
                """,
                (store_id,),
            )
            db.commit()
    except Exception as e:
        print("Error deleting store:", e)
        db.rollback()
        return False

    return True


# ====================
# Employees in a Store
# ====================


def count_employees_in_store(store: Store):
    """
    計算指定商店的員工數量

    :param store: 商店對象

    :return: 員工數量
    """
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                SELECT COUNT(*) AS count FROM employee WHERE store = %s;
                """,
                (store.id,),
            )
            row = cursor.fetchone()
    except Exception as e:
        print("Error counting employees in store:", e)
        return 0

    return row["count"] if row else 0


def get_employees_in_store(store: Store):
    """
    取得指定商店的所有員工資料

    :param store: 商店對象

    :return: 員工資料列表
    """
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM employee WHERE store = %s;
                """,
                (store.id,),
            )
            rows = cursor.fetchall()
    except Exception as e:
        print("Error fetching employees in store:", e)
        return []

    employees = []

    for row in rows:
        row["store"] = store
        employees.append(Employee.model_validate(row))

    return employees
