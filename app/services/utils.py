import io
from datetime import time, timedelta
from hashlib import sha1
from uuid import NAMESPACE_DNS, uuid5

from PIL import Image as PILImage


def convert_to_webp(image_data: bytes) -> bytes:
    """
    將圖片轉換為 WebP 格式

    :param image_data: 原始圖片的二進位資料

    :return: 轉換後的 WebP 圖片二進位資料
    """

    buf = io.BytesIO(image_data)

    with PILImage.open(buf) as img:
        webp_io = io.BytesIO()
        img.save(webp_io, format="WEBP")
        webp_data = webp_io.getvalue()
        webp_io.close()

    buf.close()

    return webp_data


def get_uuid_from_data(data: bytes) -> str:
    """
    根據圖片資料生成 UUID

    :param data: 圖片的二進位資料

    :return: 生成的 UUID 字串
    """
    hashed = sha1(data).hexdigest()
    return str(uuid5(NAMESPACE_DNS, hashed))


def timedelta_to_time(td: timedelta):
    """
    將 timedelta 轉換為時間格式

    :param td: 時間差物件

    :return: 時間字串，格式為 HH:MM:SS
    """
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return time(hour=hours, minute=minutes, second=seconds)
