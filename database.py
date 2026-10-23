"""
database.py
Connection management and schema setup for the XAMPP / MySQL database.

Author: Kenneth Panio
"""

from pathlib import Path

import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "",
    "database": "shanice",
}

SCHEMA_FILE = Path(__file__).with_name("schema.sql")


def get_connection():
    """Return a connection to the configured database (DB_CONFIG['database'])."""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        raise RuntimeError(
            f"Could not connect to MySQL. Make sure XAMPP/MySQL is running.\nDetails: {e}"
        ) from e


def setup_database():
    """Create the database and products table if they don't exist yet."""
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
        )
        schema_sql = SCHEMA_FILE.read_text(encoding="utf-8")
        with conn.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
            cursor.execute(f"USE {DB_CONFIG['database']}")
            for statement in schema_sql.split(";"):
                if statement.strip():
                    cursor.execute(statement)
        conn.commit()
        conn.close()
        print(f"Database ready: {DB_CONFIG['database']} / products table OK")
    except Error as e:
        raise RuntimeError(f"Database setup failed: {e}") from e
