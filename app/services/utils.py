import io
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
