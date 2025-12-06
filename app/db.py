import os

import pymysql

connection = None


def get_db_connection():
    global connection
    if connection:  # 重複使用已存在的連線
        return connection

    connection = pymysql.connect(
        host="localhost",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWD"),
        database=os.getenv("DB_NAME"),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )

    return connection
