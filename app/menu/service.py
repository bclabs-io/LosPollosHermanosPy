import json

from .model import Combo, Dish, Ingredient

with open("app/seeds/dish.json", "r", encoding="utf-8") as f:
    data = json.load(f)

    dishes_seed: list[Dish] = []

    for dish in data:
        ingredients = []
        for ingredient in dish["ingredients"]:
            ingredients.append(Ingredient.model_validate(ingredient))
        dish_data = {
            "id": dish["id"],
            "name": dish["name"],
            "image": dish["image"],
            "calories": dish["calories"],
            "price": dish["price"],
            "ingredients": ingredients,
        }
        dishes_seed.append(Dish.model_validate(dish_data))

    suppliers_seed = [ingredient.supplier for dish in dishes_seed for ingredient in dish.ingredients]

    suppliers_seed = list(set(suppliers_seed))
    suppliers_seed.sort()

with open("app/seeds/combo.json", "r", encoding="utf-8") as f:
    data = json.load(f)

    combos_seed: list[Combo] = []

    for combo in data:
        combo_dishes = []
        for dish_name in combo["dishes"]:
            for dish in dishes_seed:
                if dish.name == dish_name:
                    combo_dishes.append(dish)
                    break
        combo_data = {
            "id": combo["id"],
            "name": combo["name"],
            "image": combo["image"],
            "price": combo["price"],
            "dishes": combo_dishes,
        }
        combos_seed.append(Combo(**combo_data))


# ====================
# Suppliers
# ====================


def get_suppliers():
    """
    取得供應商列表
    """
    return suppliers_seed


# ====================
# Dishes
# ====================


def add_dish(dish: dict) -> Dish:
    """
    新增單點菜品

    :param dish: 菜品資料字典
    """
    dish = Dish(**dish)
    dishes_seed.append(dish)

    return dish


def get_dishes() -> list[Dish]:
    """
    取得所有單點菜品
    """
    return dishes_seed


def get_dish_by_id(dish_id: int) -> Dish | None:
    """
    取得指定 ID 的單點菜品

    :param dish_id: 菜品 ID
    """
    for dish in dishes_seed:
        if dish.id == dish_id:
            return dish
    return None


def update_dish_by_id(dish_id: int, updated_dish: dict) -> Dish | None:
    """
    更新指定 ID 的單點菜品

    :param dish_id: 菜品 ID
    :param updated_dish: 更新後的菜品資料字典
    """
    updated_dish = Dish(**updated_dish)
    for index, dish in enumerate(dishes_seed):
        if dish.id == dish_id:
            dishes_seed[index] = updated_dish
            return updated_dish
    return None


def delete_dish_by_id(dish_id: int) -> bool:
    """
    刪除指定 ID 的單點菜品

    :param dish_id: 菜品 ID
    """
    for index, dish in enumerate(dishes_seed):
        if dish.id == dish_id:
            del dishes_seed[index]
            return True
    return False


# ====================
# Combos
# ====================


def add_combo(combo: dict) -> Combo:
    """
    新增套餐
    :param combo: 套餐資料字典
    """
    combo = Combo(**combo)
    combos_seed.append(combo)
    return combo


def get_combos() -> list[Combo]:
    """
    取得所有套餐
    """
    return combos_seed


def get_combo_by_id(combo_id: int) -> Combo | None:
    """
    取得指定 ID 的套餐

    :param combo_id: 套餐 ID
    """
    for combo in combos_seed:
        if combo.id == combo_id:
            return combo
    return None


def update_combo_by_id(combo_id: int, updated_combo: dict) -> Combo | None:
    """
    更新指定 ID 的套餐

    :param combo_id: 套餐 ID
    :param updated_combo: 更新後的套餐資料字典
    """
    updated_combo = Combo(**updated_combo)
    for index, combo in enumerate(combos_seed):
        if combo.id == combo_id:
            combos_seed[index] = updated_combo
            return updated_combo
    return None


def delete_combo_by_id(combo_id: int) -> bool:
    """
    刪除指定 ID 的套餐

    :param combo_id: 套餐 ID
    """
    for index, combo in enumerate(combos_seed):
        if combo.id == combo_id:
            del combos_seed[index]
            return True
    return False
