from flask import Blueprint, abort, render_template, request, url_for

from app.services import (
    add_employee,
    delete_employee_by_id,
    get_employee_by_id,
    get_employees,
    get_employees_in_store,
    get_store_by_id,
    get_store_by_name,
    get_stores,
    update_employee_by_id,
)

employee_bp = Blueprint("employee", __name__, url_prefix="/employees")


@employee_bp.route("/")
def employees_list():
    keyword = request.args.get("query", "").strip()

    if keyword:
        store = get_store_by_name(keyword)
        if store:
            employees = get_employees_in_store(store.id)
        else:
            employees = []
    else:
        employees = get_employees()

    return render_template("employee/list.html", employees=employees, keyword=keyword)


@employee_bp.route("/<int:employee_id>")
def view_employee(employee_id: int):
    employee = get_employee_by_id(employee_id)

    if employee is None:
        abort(404)

    return render_template("employee/detail.html", employee=employee)


@employee_bp.route("/add", methods=["GET", "POST"])
def add_employee_view():
    if request.method == "POST":
        form = request.form

        data = {
            "name": form.get("name"),
            "email": form.get("email"),
            "phone": form.get("phone"),
            "store": get_store_by_id(form.get("store", type=int)),
            "position": form.get("position"),
            "type_": form.get("type"),
            "salary": form.get("salary", type=int),
            "hire_date": form.get("hire_date"),
        }

        employee = add_employee(data)
        redirect_url = url_for("employee.view_employee", employee_id=employee.id)
        return render_template("saved.html", item_name=employee.name, url=redirect_url)

    ########################################

    stores = get_stores()

    return render_template("employee/add.html", stores=stores)


@employee_bp.route("/<int:employee_id>/edit", methods=["GET", "POST"])
def edit_employee(employee_id: int):
    employee = get_employee_by_id(employee_id)

    if employee is None:
        abort(404)

    if request.method == "POST":
        form = request.form

        data = {
            "name": form.get("name"),
            "email": form.get("email"),
            "phone": form.get("phone"),
            "store": get_store_by_id(form.get("store", type=int)),
            "position": form.get("position"),
            "type_": form.get("type"),
            "salary": form.get("salary", type=int),
            "hire_date": form.get("hire_date"),
        }

        employee = update_employee_by_id(employee_id, data)
        redirect_url = url_for("employee.view_employee", employee_id=employee.id)
        return render_template("saved.html", item_name=employee.name, url=redirect_url)

    ########################################

    stores = get_stores()

    return render_template("employee/edit.html", employee=employee, stores=stores)


@employee_bp.route("/<int:employee_id>/delete")
def delete_employee(employee_id: int):
    employee = get_employee_by_id(employee_id)

    if employee is None:
        abort(404)

    delete_employee_by_id(employee_id)
    redirect_url = url_for("employee.employees_list")
    return render_template("delete-item.html", item_name=employee.name, url=redirect_url)
