from flask import Blueprint, abort

employee_bp = Blueprint("employee", __name__, url_prefix="/employees")


@employee_bp.route("/")
def employees_list():
    abort(501)  # Not implemented yet
