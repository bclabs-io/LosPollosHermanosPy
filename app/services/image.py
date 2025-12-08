from werkzeug.datastructures import FileStorage

from app.db import get_db
from app.models import Image

from .utils import convert_to_webp, get_uuid_from_data

__all__ = [
    "add_image",
    "get_image_by_id",
    "get_image_by_name",
    "delete_image_by_id",
]


def add_image(data: bytes) -> Image | None:
    """
    新增圖片

    :param data: 圖片資料字典

    :return: 新增的圖片資料
    """
    db = get_db()
    webp_data = convert_to_webp(data)
    name = f"{get_uuid_from_data(webp_data)}.webp"

    img = get_image_by_name(name=name)

    if img is not None:
        return img  # 圖片已存在，直接回傳

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO image (name, data)
                VALUES (%s, %s);
                """,
                (name, webp_data),
            )

        db.commit()
        image_id = cursor.lastrowid
    except Exception as e:
        print("Error adding image:", e)
        db.rollback()
        return None

    return get_image_by_id(image_id)


def get_image_by_id(image_id: int) -> Image | None:
    """
    透過 ID 取得圖片資料

    :param image_id: 圖片 ID

    :return: 圖片資料或 None
    """
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM image WHERE id = %s;", (image_id,))
            row = cursor.fetchone()
    except Exception as e:
        print("Error fetching image by id:", e)
        return None

    if row is None:
        return None

    image = Image.model_validate(row)
    return image


def get_image_by_name(name: str) -> Image | None:
    """
    透過名稱取得圖片資料

    :param name: 圖片名稱

    :return: 圖片資料或 None
    """
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM image WHERE name = %s;", (name,))
            row = cursor.fetchone()
    except Exception as e:
        print("Error fetching image by name:", e)
        return None

    if row is None:
        return None

    image = Image.model_validate(row)
    return image


def delete_image_by_id(image_id: int) -> bool:
    """
    刪除指定 ID 的圖片

    :param image_id: 圖片 ID

    :return: 是否刪除成功
    """
    db = get_db()
    try:
        with db.cursor() as cursor:
            cursor.execute("DELETE FROM image WHERE id = %s;", (image_id,))
            db.commit()

            return cursor.rowcount > 0
    except Exception as e:
        print("Error deleting image:", e)
        db.rollback()
        return False


# ====================
# Helpers
# ====================


def process_image_upload(data: dict, default_path=""):
    """
    處理可能有的圖片上傳，並修改成圖片網址
    """

    if "image" not in data:
        data["image_url"] = default_path
        return data

    if isinstance(data["image"], bytes):
        buf = data["image"]
    elif isinstance(data["image"], FileStorage):
        # 上傳的是檔案物件
        buf = data["image"].stream.read()

    img = add_image(buf)
    data["image_url"] = "/images/" + img.name
    del data["image"]

    return data
