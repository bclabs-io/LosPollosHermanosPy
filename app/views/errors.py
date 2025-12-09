from flask import Blueprint, render_template

error_bp = Blueprint("error", __name__)


@error_bp.app_errorhandler(400)
def bad_request(e):
    """
    這裡渲染的是 400.html 頁面
    """
    return render_template("errors/400.html"), 400


@error_bp.app_errorhandler(404)
def page_not_found(e):
    """
    這裡渲染的是 404.html 頁面
    """
    return render_template("errors/404.html"), 404


@error_bp.app_errorhandler(405)
def method_not_allowed(e):
    """
    這裡渲染的是 405.html 頁面
    """
    return render_template("errors/405.html"), 405


@error_bp.app_errorhandler(418)
def im_a_teapot(e):
    """
    這裡渲染的是 418.html 頁面
    """
    return render_template("errors/418.html"), 418


@error_bp.app_errorhandler(500)
def internal_server_error(e):
    """
    這裡渲染的是 500.html 頁面
    """
    return render_template("errors/500.html"), 500


@error_bp.app_errorhandler(501)
def not_implemented(e):
    """
    這裡渲染的是 501.html 頁面
    """
    return render_template("errors/501.html"), 501


@error_bp.app_errorhandler(503)
def service_unavailable(e):
    """
    這裡渲染的是 503.html 頁面
    """
    return render_template("errors/503.html"), 503
