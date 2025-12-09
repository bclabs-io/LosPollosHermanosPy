from flask import Blueprint, abort, render_template, request, url_for

from app.services import (
    add_store,
    delete_store_by_id,
    get_store_by_id,
    get_stores,
    get_stores_nearby,
    update_store_by_id,
)

store_bp = Blueprint("store", __name__, url_prefix="/stores")

weekdays_map = {
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday",
    7: "Sunday",
}


@store_bp.route("/")
def stores_list():
    keyword = request.args.get("query", "").strip()

    stores = get_stores(keyword)

    return render_template("store/list.html", stores=stores, keyword=keyword)


@store_bp.route("/nearby")
def stores_nearby():
    latitude = request.args.get("latitude", type=float)
    longitude = request.args.get("longitude", type=float)
    radius = request.args.get("radius", default=10.0, type=float)
    keyword = request.args.get("query", "").strip()

    stores = get_stores_nearby(latitude, longitude, radius_km=radius, keyword=keyword)

    return render_template("store/list-nearby.html", stores=stores, keyword=keyword)


@store_bp.route("/<int:store_id>")
def view_store(store_id: int):
    store = get_store_by_id(store_id)

    if store is None:
        return abort(404)

    weekdays = [weekdays_map.get(day, "Unknown") for day in store.weekdays]
    weekdays = ", ".join(weekdays)

    return render_template("store/detail.html", store=store, weekdays=weekdays)


@store_bp.route("/add", methods=["GET", "POST"])
def add_store_view():
    if request.method == "POST":
        form = request.form

        data = {
            "name": form.get("name", ""),
            "phone": form.get("phone", ""),
            "state": form.get("state", ""),
            "city": form.get("city", ""),
            "address": form.get("address", ""),
            "zipcode": form.get("zipcode", ""),
            "latitude": float(form.get("latitude", "")),
            "longitude": float(form.get("longitude", "")),
            "weekdays": list(map(int, form.getlist("weekdays"))),
            "open_time": form.get("open_time", ""),
            "close_time": form.get("close_time", ""),
        }

        new_store = add_store(data)
        redirect_url = url_for("store.view_store", store_id=new_store.id)
        return render_template("saved.html", item_name=new_store.name, url=redirect_url)

    ########################################

    return render_template("store/add.html", weekdays_map=weekdays_map)


@store_bp.route("/<int:store_id>/edit", methods=["GET", "POST"])
def edit_store(store_id: int):
    store = get_store_by_id(store_id)

    if store is None:
        return abort(404)

    ########################################

    if request.method == "POST":
        form = request.form

        data = {
            "name": form.get("name", ""),
            "phone": form.get("phone", ""),
            "state": form.get("state", ""),
            "city": form.get("city", ""),
            "address": form.get("address", ""),
            "zipcode": form.get("zipcode", ""),
            "latitude": float(form.get("latitude", "")),
            "longitude": float(form.get("longitude", "")),
            "weekdays": list(map(int, form.getlist("weekdays"))),
            "open_time": form.get("open_time", ""),
            "close_time": form.get("close_time", ""),
        }

        print(data)

        updated_store = update_store_by_id(store_id, data)
        redirect_url = url_for("store.view_store", store_id=updated_store.id)
        return render_template("saved.html", item_name=updated_store.name, url=redirect_url)

    ########################################

    return render_template("store/edit.html", store=store, weekdays_map=weekdays_map)


@store_bp.route("/<int:store_id>/delete")
def delete_store_view(store_id: int):
    store = get_store_by_id(store_id)

    if store is None:
        return abort(404)

    delete_store_by_id(store_id)
    redirect_url = url_for("store.stores_list")
    return render_template("delete-item.html", item_name=store.name, url=redirect_url)
