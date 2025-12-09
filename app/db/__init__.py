import os

import pymysql


def get_db():
    """
    取得資料庫連線
    """
    # global connection
    # if connection:  # 重複使用已存在的連線
    #     return connection

    connection = pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWD"),
        database=os.getenv("DB_NAME"),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )

    return connection


def create_tables():
    """
    建立資料表
    """
    db = get_db()

    with db.cursor() as cursor:
        with open("app/schema.sql", "r", encoding="utf-8") as f:
            sql_statements = f.read()
            for statement in sql_statements.split(";"):
                stmt = statement.strip()
                if stmt:
                    cursor.execute(stmt)

        db.commit()


def drop_table(table_name: str):
    """
    刪除指定資料表

    :param table_name: 要刪除的資料表名稱
    """
    db = get_db()

    with db.cursor() as cursor:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
        db.commit()


def drop_all_tables():
    """
    刪除所有資料表
    """
    db = get_db()

    with db.cursor() as cursor:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")  # 關閉外鍵檢查
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        for table in tables:
            table_name = list(table.values())[0]
            cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")  # 開啟外鍵檢查

        db.commit()
