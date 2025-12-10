from datetime import date

from app.db import get_db
from app.models import Employee

from .store import get_store_by_id

__all__ = [
    "add_employee",
    "get_employees",
    "get_employee_by_id",
    "get_employee_by_email",
    "update_employee_by_id",
    "delete_employee_by_id",
    "get_positions",
    "count_employees_by_position",
    "get_employees_by_position",
]


def add_employee(data: dict):
    """
    新增員工

    :param data: 員工資料字典

    :return: 新增的員工資料或 None
    """
    db = get_db()

    data["hire_date"] = date.strptime(data["hire_date"], "%Y-%m-%d")

    # 驗證資料
    employee = Employee.model_validate(data)

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO employee (name, position, salary, email, phone, hireDate, type, store)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """,
                (
                    employee.name,
                    employee.position,
                    employee.salary,
                    employee.email,
                    employee.phone,
                    employee.hire_date,
                    employee.type_,
                    employee.store.id if employee.store else None,
                ),
            )
            db.commit()
            employee_id = cursor.lastrowid
    except Exception as e:
        print(f"Error adding employee: {e}")
        db.rollback()
        return None

    employee = get_employee_by_id(employee_id)
    return employee


def get_employees():
    """
    取得所有員工資料

    :return: 員工資料列表
    """
    db = get_db()
    employees = []

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM employee;
                """
            )
            rows = cursor.fetchall()
    except Exception as e:
        print("Error fetching employees:", e)
        return []

    for row in rows:
        row["store"] = get_store_by_id(row["store"]) if row["store"] else None
        row["store"] = get_store_by_id(row["store"]) if row["store"] else None
        row["hire_date"] = row["hireDate"]
        row["type_"] = row["type"]
        employees.append(Employee.model_validate(row))

    return employees


def get_employee_by_id(employee_id: int):
    """
    根據員工 ID 獲取員工資訊

    :param employee_id: 員工 ID

    :return: Employee 對象或 None
    """
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM employee WHERE id = %s;
                """,
                (employee_id,),
            )
            row = cursor.fetchone()
    except Exception as e:
        print(f"Error fetching employee by id: {e}")
        return None

    if row is None:
        return None

    row["store"] = get_store_by_id(row["store"]) if row["store"] else None
    row["hire_date"] = row["hireDate"]
    row["type_"] = row["type"]
    employee = Employee.model_validate(row)

    return employee


def get_employee_by_email(email: str):
    """
    根據員工電子郵件獲取員工資訊

    :param email: 員工電子郵件

    :return: Employee 對象或 None
    """
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM employee WHERE email = %s;
                """,
                (email,),
            )
            row = cursor.fetchone()
    except Exception as e:
        print(f"Error fetching employee by email: {e}")
        return None

    if row is None:
        return None

    row["store"] = get_store_by_id(row["store"]) if row["store"] else None
    row["hire_date"] = row["hireDate"]
    row["type_"] = row["type"]
    employee = Employee.model_validate(row)

    return employee


def update_employee_by_id(employee_id: int, data: dict):
    """
    更新員工資料

    :param employee_id: 員工 ID
    :param data: 欲更新的員工資料字典

    :return: 更新後的員工資料或 None
    """
    db = get_db()

    # 驗證資料
    employee = Employee.model_validate(data)

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                UPDATE employee SET name = %s, position = %s, email = %s, phone = %s,
                    hireDate = %s, type = %s, store = %s
                WHERE id = %s;
                """,
                (
                    employee.name,
                    employee.position,
                    employee.email,
                    employee.phone,
                    employee.hire_date,
                    employee.type_,
                    employee.store.id if employee.store else None,
                    employee_id,
                ),
            )
            db.commit()
    except Exception as e:
        print(f"Error updating employee: {e}")
        db.rollback()
        return None

    return get_employee_by_id(employee_id)


def delete_employee_by_id(employee_id: int):
    """
    刪除員工資料

    :param employee_id: 員工 ID

    :return: 是否刪除成功
    """
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM employee WHERE id = %s;
                """,
                (employee_id,),
            )
            db.commit()
    except Exception as e:
        print(f"Error deleting employee: {e}")
        db.rollback()
        return False

    return True


# ===================
# Employees by Position
# ===================


def get_positions():
    """
    取得所有職位名稱

    :return: 職位名稱列表
    """
    db = get_db()
    employees = []

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                SELECT DISTINCT position FROM employee;
                """
            )
            rows = cursor.fetchall()
    except Exception as e:
        print("Error fetching positions:", e)
        return []

    for row in rows:
        employees.append(row["position"])

    return employees


def count_employees_by_position(position: str):
    """
    計算指定職位的員工數量

    :param position: 職位名稱

    :return: 員工數量
    """
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                SELECT position, COUNT(*) AS count FROM employee
                WHERE position = %s
                GROUP BY position;
                """,
                (position,),
            )
            row = cursor.fetchone()
    except Exception as e:
        print("Error counting employees by position:", e)
        return 0

    return row["count"] if row else 0


def get_employees_by_position(position: str):
    """
    取得指定職位的所有員工資料

    :param position: 職位名稱

    :return: 員工資料列表
    """
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM employee WHERE position = %s;
                """,
                (position,),
            )
            rows = cursor.fetchall()
    except Exception as e:
        print("Error fetching employees by position:", e)
        return []

    employees = []
    for row in rows:
        row["store"] = get_store_by_id(row["store"]) if row["store"] else None
        row["store"] = get_store_by_id(row["store"]) if row["store"] else None
        row["hire_date"] = row["hireDate"]
        row["type_"] = row["type"]
        employees.append(Employee.model_validate(row))

    return employees
