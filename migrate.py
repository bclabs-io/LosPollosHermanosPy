import json
import os
from collections import defaultdict

from dotenv import load_dotenv

load_dotenv()

from app.db import create_tables, drop_all_tables
from app.services import (
    add_combo,
    add_dish,
    add_dish_to_combo,
    add_image,
    add_ingredient,
    add_ingredient_to_dish,
    add_ingredient_to_supplier,
    add_supplier,
)

mappings = defaultdict(dict)


def seed_images():
    """
    初始化圖片種子資料
    """
    print("Seeding images...")

    images = os.listdir("seeds/images")

    print(f"Loaded {len(images)} image files.")
    for file in images:
        if file == ".DS_Store":
            continue  # Skip system file
        with open(os.path.join("seeds/images", file), "rb") as f:
            img_data = f.read()
            img = add_image(img_data)
            mappings["img"][file] = img.name

    print("Done.")


def seed_suppliers():
    """
    初始化供應商種子資料
    """
    print("Seeding suppliers...")

    with open("seeds/supplier.json", "r", encoding="utf-8") as f:
        suppliers_data = json.load(f)

    print(f"Loaded {len(suppliers_data)} suppliers from JSON.")

    for supplier_data in suppliers_data:
        supplier_data["image_url"] = "/images/" + mappings["img"].get(supplier_data["image"])
        supplier = add_supplier(supplier_data)
        mappings["sup"][supplier.name] = supplier

        # 加入食材 & 供應商關聯
        for ingredient_name in supplier_data.get("produce", []):
            ingredient_id = mappings["ing"].get(ingredient_name)

            if not ingredient_id:  # 如果食材不存在，則新增
                ingredient = add_ingredient({"name": ingredient_name})
                ingredient_id = ingredient.id
                mappings["ing"][ingredient.name] = ingredient

            add_ingredient_to_supplier(supplier, ingredient)

    print("Done.")


def seed_dishes():
    """
    初始化餐點種子資料
    """
    print("Seeding dishes...")

    with open("seeds/dish.json", "r", encoding="utf-8") as f:
        dishes_data = json.load(f)

    print(f"Loaded {len(dishes_data)} dishes from JSON.")

    for dish_data in dishes_data:
        dish_data["image_url"] = "/images/" + mappings["img"].get(dish_data["image"])
        dish = add_dish(dish_data)
        mappings["dish"][dish.name] = dish

        # 加入食材到菜品關聯
        for ingredient in dish_data.get("ingredients", []):
            name = ingredient["name"]
            quantity = ingredient["quantity"]
            unit = ingredient["unit"]

            ingredient = mappings["ing"].get(name)

            if not ingredient:
                ingredient = add_ingredient({"name": name})
                mappings["ing"][ingredient.name] = ingredient

            add_ingredient_to_dish(dish, ingredient, quantity, unit)

    print("Done.")


def seed_combos():
    """
    初始化套餐種子資料
    """
    print("Seeding combos...")

    with open("seeds/combo.json", "r", encoding="utf-8") as f:
        combos_data = json.load(f)

    print(f"Loaded {len(combos_data)} combos from JSON.")

    for combo_data in combos_data:
        combo_data["image_url"] = "/images/" + mappings["img"].get(combo_data["image"])
        combo_data["dishes"] = [mappings["dish"][dish_name] for dish_name in combo_data.get("dishes", [])]

        combo = add_combo(combo_data)
        mappings["combo"][combo.name] = combo

        # 加入菜品到套餐關聯
        for dish in combo_data.get("dishes", []):
            add_dish_to_combo(combo, dish)

    print("Done.")


if __name__ == "__main__":
    drop_all_tables()  # 先刪除所有表格
    create_tables()  # 再重新建立所有表格

    # 初始化種子資料
    seed_funcs = [seed_images, seed_suppliers, seed_dishes, seed_combos]

    for func in seed_funcs:
        func()
        print("=" * 40)

    print("Database migration completed.")
