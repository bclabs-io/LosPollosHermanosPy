import json
import os
from collections import defaultdict

from dotenv import load_dotenv

load_dotenv()

from app.db import create_tables, drop_all_tables
from app.services import add_combo, add_dish, add_image, add_store, add_supplier

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


def seed_stores():
    """
    初始化商店種子資料
    """
    print("Seeding stores...")

    with open("seeds/store.json", "r", encoding="utf-8") as f:
        stores_data = json.load(f)

    print(f"Loaded {len(stores_data)} stores from JSON.")

    for store_data in stores_data:
        store = add_store(store_data)
        mappings["store"][store.name] = store

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
        del supplier_data["image"]
        supplier = add_supplier(supplier_data)
        mappings["sup"][supplier.name] = supplier

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
        del dish_data["image"]
        dish = add_dish(dish_data)
        mappings["dish"][dish.name] = dish

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
        del combo_data["image"]
        combo = add_combo(combo_data)
        mappings["combo"][combo.name] = combo

    print("Done.")


if __name__ == "__main__":
    drop_all_tables()  # 先刪除所有表格
    create_tables()  # 再重新建立所有表格

    # 初始化種子資料
    seed_funcs = [seed_images, seed_stores, seed_suppliers, seed_dishes, seed_combos]

    for func in seed_funcs:
        func()
        print("=" * 40)

    print("Database migration completed.")
