import os

import pymysql

connection = None


def get_db():
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


def create_tables():
    conn = get_db()
    drop_all_tables()
    with conn.cursor() as cursor:
        with open("app/schema.sql", "r", encoding="utf-8") as f:
            sql_statements = f.read()
            for statement in sql_statements.split(";"):
                stmt = statement.strip()
                if stmt:
                    cursor.execute(stmt)
    conn.commit()


def drop_table(table_name: str):
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
    conn.commit()


def drop_all_tables():
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        for table in tables:
            table_name = list(table.values())[0]
            cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
    conn.commit()
