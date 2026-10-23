"""
main.py
Interactive CLI menu for the product CRUD system.
Kept thin on purpose: it only mixes user input with repository calls,
using helpers from utils.py.

Run:  python main.py
Author: Kenneth Panio
"""

from database import setup_database
from products import (
    delete_product,
    get_all_products,
    get_product,
    insert_product,
    update_product,
)
from utils import ask_name, ask_price, format_peso

TABLE_HEADER = "{:<6} {:<30} {:>12}".format("ID", "PRODUCT NAME", "PRICE (PHP)")
TABLE_ROW = "{:<6} {:<30} {:>12}"


def ask_id(action):
    """Prompt for an existing product id, or None to cancel."""
    raw = input(f"Enter product ID to {action} (or blank to cancel): ").strip()
    if not raw:
        return None
    if not raw.isdigit():
        print("ID must be a number.")
        return None
    product_id = int(raw)
    if get_product(product_id) is None:
        print(f"No product found with ID {product_id}.")
        return None
    return product_id


def print_table(products):
    if not products:
        print("\nNo products yet. Add one first!")
        return
    print("\n" + TABLE_HEADER)
    print("-" * 50)
    for pid, name, price in products:
        print(TABLE_ROW.format(pid, name[:28], format_peso(price)))
    print(f"\nTotal products: {len(products)}")


def handle_add():
    print("\n--- Add Product ---")
    name = ask_name()
    price = ask_price()
    pid = insert_product(name, price)
    print(f"Added: {name} at {format_peso(price)} (ID {pid})")


def handle_list():
    print("\n--- Product List ---")
    print_table(get_all_products())


def handle_update():
    print("\n--- Update Product ---")
    pid = ask_id("update")
    if pid is None:
        return
    _, current_name, current_price = get_product(pid)
    print("(Press Enter to keep the current value)")
    name = ask_name(current_name)
    price = ask_price(current_price)
    update_product(pid, name, price)
    print(f"Updated ID {pid}: {name} at {format_peso(price)}")


def handle_delete():
    print("\n--- Delete Product ---")
    pid = ask_id("delete")
    if pid is None:
        return
    _, name, _ = get_product(pid)
    confirm = input(f"Delete '{name}'? (y/n): ").strip().lower()
    if confirm == "y":
        delete_product(pid)
        print("Deleted.")
    else:
        print("Cancelled.")


MENU = {
    "1": (handle_add, "Add product"),
    "2": (handle_list, "View products"),
    "3": (handle_update, "Update product"),
    "4": (handle_delete, "Delete product"),
}


def show_menu():
    print("\n===== PRODUCT CRUD (PHP) =====")
    for key, (_, label) in sorted(MENU.items()):
        print(f"{key}. {label}")
    print("5. Exit")


def main():
    setup_database()
    while True:
        show_menu()
        choice = input("Choose (1-5): ").strip()
        if choice == "5":
            print("Goodbye!")
            break
        if choice in MENU:
            MENU[choice][0]()
        else:
            print("Invalid choice. Enter 1-5.")


if __name__ == "__main__":
    main()
