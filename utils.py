"""
utils.py
Shared helpers: currency formatting and free-of-DB input validation.
Anything that needs the database stays in main.py.

Author: Kenneth Panio
"""


def format_peso(amount):
    """Format a number as Philippine Peso, e.g. ₱1,250.50"""
    return f"₱{float(amount):,.2f}"


def ask_name(current=None):
    """Prompt for a product name (blank keeps the current one when updating)."""
    prompt = f"Product name [{current}]: " if current else "Product name: "
    name = input(prompt).strip()
    if current and not name:
        return current
    while not name:
        print("Name cannot be empty.")
        name = input("Product name: ").strip()
    return name


def ask_price(current=None):
    """Prompt for a price in PHP (blank keeps the current one when updating)."""
    default = f" [{current}]" if current is not None else ""
    while True:
        raw = input(f"Price (PHP){default}: ").strip()
        if current is not None and not raw:
            return current
        try:
            price = float(raw.replace("₱", "").replace(",", ""))
        except ValueError:
            print("Please enter a valid number, e.g. 1499.99")
            continue
        if price < 0:
            print("Price cannot be negative.")
            continue
        return price
