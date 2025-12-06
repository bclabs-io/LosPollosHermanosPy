from flask import Blueprint, render_template

error_bp = Blueprint("error", __name__)


@error_bp.app_errorhandler(404)
def page_not_found(e):
    # 這裡渲染的是 404.html 頁面
    return render_template("errors/404.html"), 404


@error_bp.app_errorhandler(418)
def im_a_teapot(e):
    # 這裡渲染的是 418.html 頁面
    return render_template("errors/418.html"), 418


@error_bp.app_errorhandler(500)
def internal_server_error(e):
    # 這裡渲染的是 500.html 頁面
    return render_template("errors/500.html"), 500
