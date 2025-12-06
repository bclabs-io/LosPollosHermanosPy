from flask import Blueprint, abort, redirect, render_template, request, url_for

menu_bp = Blueprint("menu", __name__, url_prefix="/menu")


dishes_seed = [
    {
        "id": 1,
        "name": "Burger",
        "image": "burger.webp",
        "ingredients": [
            {"name": "Beef patty", "quantity": 1, "unit": "piece", "supplier": "Happy Cows Farm"},
            {"name": "Cheese", "quantity": 1, "unit": "slice", "supplier": "Dairy Best"},
            {"name": "Lettuce", "quantity": 1, "unit": "leaf", "supplier": "Fresh Greens Co."},
            {"name": "Tomato", "quantity": 1, "unit": "slice", "supplier": "Veggie Delight"},
            {"name": "Onions", "quantity": 1, "unit": "slice", "supplier": "Onion World"},
            {"name": "Pickles", "quantity": 1, "unit": "slice", "supplier": "Pickle Palace"},
            {"name": "Special sauce", "quantity": 1, "unit": "serving", "supplier": "Sauce Factory"},
            {"name": "Toasted brioche bun", "quantity": 1, "unit": "piece", "supplier": "Bun Bakery"},
        ],
        "calories": 600,
        "price": 8.99,
    },
    {
        "id": 2,
        "name": "Bacon Burger",
        "image": "bacon_burger.webp",
        "ingredients": [
            {"name": "Bacon", "quantity": 1, "unit": "slice", "supplier": "Bacon World"},
            {"name": "Cheese", "quantity": 1, "unit": "slice", "supplier": "Dairy Best"},
            {"name": "Lettuce", "quantity": 1, "unit": "leaf", "supplier": "Fresh Greens Co."},
            {"name": "Garlic powder", "quantity": 1, "unit": "teaspoon", "supplier": "Spice House"},
            {"name": "Paprika", "quantity": 1, "unit": "teaspoon", "supplier": "Spice House"},
            {"name": "Celery sticks", "quantity": 1, "unit": "piece", "supplier": "Fresh Greens Co."},
            {"name": "Ranch dressing", "quantity": 1, "unit": "serving", "supplier": "Ranch Factory"},
        ],
        "calories": 450,
        "price": 7.49,
    },
    {
        "id": 3,
        "name": "Fries",
        "image": "fries.webp",
        "ingredients": [
            {"name": "Potatoes", "quantity": 1, "unit": "piece", "supplier": "Potato Farm"},
            {"name": "Salt", "quantity": 1, "unit": "teaspoon", "supplier": "Spice House"},
            {"name": "Vegetable oil", "quantity": 1, "unit": "serving", "supplier": "Oil Co."},
        ],
        "calories": 300,
        "price": 3.49,
    },
    {
        "id": 4,
        "name": "Vanilla Shake",
        "image": "vanilla_shake.webp",
        "ingredients": [
            {"name": "Vanilla ice cream", "quantity": 300, "unit": "gram", "supplier": "Ice Cream Co."},
            {"name": "Milk", "quantity": 500, "unit": "ml", "supplier": "Dairy Best"},
            {"name": "Sugar", "quantity": 50, "unit": "gram", "supplier": "Sugar Supplier"},
        ],
        "calories": 500,
        "price": 4.99,
    },
    {
        "id": 5,
        "name": "Chocolate Shake",
        "image": "chocolate_shake.webp",
        "ingredients": [
            {"name": "Chocolate ice cream", "quantity": 300, "unit": "gram", "supplier": "Ice Cream Co."},
            {"name": "Milk", "quantity": 500, "unit": "ml", "supplier": "Dairy Best"},
            {"name": "Sugar", "quantity": 50, "unit": "gram", "supplier": "Sugar Supplier"},
        ],
        "calories": 550,
        "price": 5.49,
    },
    {
        "id": 6,
        "name": "Soft Drinks",
        "image": "soft_drinks.webp",
        "ingredients": [
            {"name": "Carbonated water", "quantity": 500, "unit": "ml", "supplier": "Coca-Cola Co."},
            {"name": "Sugar", "quantity": 50, "unit": "gram", "supplier": "Coca-Cola Co."},
            {"name": "Flavoring", "quantity": 1, "unit": "serving", "supplier": "Coca-Cola Co."},
        ],
        "calories": 200,
        "price": 1.99,
    },
    {
        "id": 7,
        "name": "Bottled Water",
        "image": "bottled_water.webp",
        "ingredients": [
            {"name": "Water", "quantity": 500, "unit": "ml", "supplier": "Water Supplier"},
        ],
        "calories": 0,
        "price": 0.99,
    },
]

combos_seed = [
    {
        "id": 1,
        "name": "Burger Meal",
        "image": "burger_combo.webp",
        "dishs": [
            {"name": "Burger", "quantity": 1},
            {"name": "Fries", "quantity": 1},
            {"name": "Soft Drink", "quantity": 1},
        ],
        "price": 12.99,
    },
    {
        "id": 2,
        "name": "Bacon Burger Meal",
        "image": "bacon_burger_combo.webp",
        "dishs": [
            {"name": "Bacon Burger", "quantity": 1},
            {"name": "Fries", "quantity": 1},
            {"name": "Soft Drink", "quantity": 1},
        ],
        "price": 11.99,
    },
    {
        "id": 3,
        "name": "Shake M",
        "image": "shake_combo.webp",
        "dishs": [
            {"name": "Vanilla Shake", "quantity": 1},
            {"name": "Fries", "quantity": 1},
        ],
        "price": 7.49,
    },
]


@menu_bp.route("/")
def menu():
    dishes = dishes_seed
    combos = combos_seed

    return render_template("menu/menu.html", dishes=dishes, combos=combos)


@menu_bp.route("/dish/<int:dish_id>/edit", methods=["GET", "POST"])
def edit_dish(dish_id):
    if request.method == "POST":
        # 儲存修改後的菜品資訊
        # Handle form submission to update dish details
        return redirect(url_for("menu.menu"))

    # 顯示編輯表單
    data = None

    for dish in dishes_seed:
        if dish["id"] == dish_id:
            data = dish
            break

    if data is None:
        abort(404)

    return render_template("menu/edit-dish.html", data=data)


@menu_bp.route("/dish/<int:dish_id>/delete")
def delete_dish(dish_id):
    for dish in dishes_seed:
        if dish["id"] == dish_id:
            dish_name = dish["name"]
            break
    # Placeholder for delete functionality
    return render_template("delete-item.html", item_name=dish_name, url=url_for("menu.menu"))


@menu_bp.route("/combo/<int:combo_id>/delete")
def delete_combo(combo_id):
    for combo in combos_seed:
        if combo["id"] == combo_id:
            combo_name = combo["name"]
            break
    # Placeholder for delete functionality
    return render_template("delete-item.html", item_name=combo_name, url=url_for("menu.menu"))
