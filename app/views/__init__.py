from flask import Flask

from .combo import combo_bp
from .errors import error_bp
from .image import image_bp
from .ingredient import ingredient_bp
from .location import location_bp
from .menu import menu_bp
from .supplier import supplier_bp


def register(app: Flask):
    app.register_blueprint(combo_bp)
    app.register_blueprint(error_bp)
    app.register_blueprint(image_bp)
    app.register_blueprint(ingredient_bp)
    app.register_blueprint(location_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(supplier_bp)
