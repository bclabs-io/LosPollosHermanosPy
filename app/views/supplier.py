from flask import Blueprint, abort, render_template, request, url_for

from app.services import add_supplier, delete_supplier_by_id, get_supplier_by_id, get_suppliers, update_supplier_by_id

supplier_bp = Blueprint("supplier", __name__, url_prefix="/suppliers")


@supplier_bp.route("/")
def suppliers():
    """
    供應商列表頁面
    """
    keyword = request.args.get("query", "")
    suppliers = get_suppliers(keyword=keyword)

    return render_template("supplier/list.html", suppliers=suppliers, keyword=keyword)


@supplier_bp.route("/<int:supplier_id>")
def view_supplier(supplier_id: int):
    """
    供應商詳細頁面
    """
    supplier = get_supplier_by_id(supplier_id)

    if supplier is None:
        abort(404)

    return render_template("supplier/detail.html", supplier=supplier)


@supplier_bp.route("/add", methods=["GET", "POST"])
def add_supplier_view():
    """
    新增供應商頁面
    """
    if request.method == "POST":
        form = request.form

        data = {
            "name": form.get("name", ""),
            "description": form.get("description", ""),
            "contact_person": form.get("contact_person", ""),
            "email": form.get("email", ""),
            "phone": form.get("phone", ""),
            "state": form.get("state", ""),
            "city": form.get("city", ""),
            "address": form.get("address", ""),
            "image": request.files.get("image"),
            "ingredients": form.getlist("ingredients[]"),
        }

        supplier = add_supplier(data)

        return render_template(
            "saved.html", item_name=supplier.name, url=url_for("supplier.view_supplier", supplier_id=supplier.id)
        )

    ########################################

    return render_template("supplier/add.html")


@supplier_bp.route("/<int:supplier_id>/edit", methods=["GET", "POST"])
def edit_supplier(supplier_id: int):
    """
    編輯供應商頁面
    """
    supplier = get_supplier_by_id(supplier_id)

    if supplier is None:
        abort(404)

    if request.method == "POST":
        form = request.form

        data = {
            "name": form.get("name", ""),
            "description": form.get("description", ""),
            "contact_person": form.get("contact_person", ""),
            "email": form.get("email", ""),
            "phone": form.get("phone", ""),
            "state": form.get("state", ""),
            "city": form.get("city", ""),
            "address": form.get("address", ""),
            "image": request.files.get("image"),
            "ingredients": form.getlist("ingredients[]"),
        }

        supplier = update_supplier_by_id(supplier_id, data)

        return render_template(
            "saved.html", item_name=supplier.name, url=url_for("supplier.view_supplier", supplier_id=supplier_id)
        )

    ########################################

    return render_template("supplier/edit.html", supplier=supplier)


@supplier_bp.route("/<int:supplier_id>/delete")
def delete_supplier(supplier_id: int):
    """
    刪除供應商頁面
    """
    supplier = get_supplier_by_id(supplier_id)

    if supplier is None:
        abort(404)

    delete_supplier_by_id(supplier_id)

    return render_template("delete-item.html", item_name=supplier.name, url=url_for("supplier.suppliers"))
