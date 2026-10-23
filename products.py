"""
products.py
Data-access layer: all SQL for products lives here.

Author: Kenneth Panio
"""

from database import get_connection


def insert_product(name, price):
    """CREATE - add a new product. Returns the new id."""
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO products (name, price) VALUES (%s, %s)", (name, price)
        )
        conn.commit()
        product_id = cursor.lastrowid
    conn.close()
    return product_id


def get_all_products():
    """READ - return all products as a list of (id, name, price)."""
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, name, price FROM products ORDER BY id")
        rows = cursor.fetchall()
    conn.close()
    return rows


def get_product(product_id):
    """READ - return one product by id, or None if not found."""
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT id, name, price FROM products WHERE id = %s", (product_id,)
        )
        row = cursor.fetchone()
    conn.close()
    return row


def update_product(product_id, name, price):
    """UPDATE - change a product's name and/or price. Returns True if updated."""
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute(
            "UPDATE products SET name = %s, price = %s WHERE id = %s",
            (name, price, product_id),
        )
        conn.commit()
        updated = cursor.rowcount > 0
    conn.close()
    return updated


def delete_product(product_id):
    """DELETE - remove a product by id. Returns True if deleted."""
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
        conn.commit()
        deleted = cursor.rowcount > 0
    conn.close()
    return deleted
