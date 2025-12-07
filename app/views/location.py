from flask import Blueprint, render_template, request

from app.db import get_db

location_bp = Blueprint("location", __name__, url_prefix="/location")
db = get_db()


@location_bp.route("/", methods=["GET", "POST"])
def location():
    # 處理新增位置的表單提交
    if request.method == "POST":
        form = request.form
        lat = form.get("latitude")
        lon = form.get("longitude")
        city = form.get("city")
        address = form.get("address")
        zip = form.get("zip")
        days = form.getlist("days")
        open = form.get("open")
        close = form.get("close")

        print(
            f"Received location data: lat={lat}, lon={lon}, city={city}, address={address}, zip={zip}, "
            f"days={days}, open={open}, close={close}"
        )

        with db.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO location (
                    latitude, longitude,
                    city, address, zipcode,
                    mon, tue, wed, thu, fri, sat, sun,
                    open_time, close_time
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    lat,
                    lon,
                    city,
                    address,
                    zip,
                    1 if "mon" in days else 0,
                    1 if "tue" in days else 0,
                    1 if "wed" in days else 0,
                    1 if "thu" in days else 0,
                    1 if "fri" in days else 0,
                    1 if "sat" in days else 0,
                    1 if "sun" in days else 0,
                    open,
                    close,
                ),
            )
        db.commit()

    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM location;")
        locations = cursor.fetchall()

    print(f"Fetched locations: {locations}")

    return render_template("location.html", locations=locations)
