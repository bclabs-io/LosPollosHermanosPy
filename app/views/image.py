from random import random

from flask import Blueprint, abort

from app.services import delete_image_by_id, get_image_by_name

image_bp = Blueprint("image", __name__, url_prefix="/images")


@image_bp.route("/", methods=["POST"])
def upload_image():
    if random() < 0.1:
        abort(418)

    abort(501)  # Not Implemented


@image_bp.route("/<string:name>", methods=["GET"])
def view_image(name):
    image = get_image_by_name(name)

    if image is None:
        abort(404)

    return image.data, 200, {"Content-Type": "image/webp"}


@image_bp.route("/<string:name>", methods=["DELETE"])
def delete_image(name):
    image = get_image_by_name(name)

    if image is None:
        abort(404)

    success = delete_image_by_id(image.id)

    if not success:
        abort(500)

    return "", 204
