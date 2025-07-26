import sqlite3

def create_tables(conn):
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        cost REAL,
        category TEXT,
        name TEXT,
        brand TEXT,
        retail_price REAL,
        department TEXT,
        sku TEXT,
        distribution_center_id INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        email TEXT,
        age INTEGER,
        gender TEXT,
        state TEXT,
        street_address TEXT,
        postal_code TEXT,
        city TEXT,
        country TEXT,
        latitude REAL,
        longitude REAL,
        traffic_source TEXT,
        created_at TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        status TEXT,
        gender TEXT,
        created_at TEXT,
        returned_at TEXT,
        shipped_at TEXT,
        delivered_at TEXT,
        num_of_item INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        product_id INTEGER,
        user_id INTEGER,
        size TEXT,
        price REAL,
        quantity INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory_items (
        inventory_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        created_at TEXT,
        stock INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS distribution_centers (
        id INTEGER PRIMARY KEY,
        name TEXT,
        latitude REAL,
        longitude REAL
    )
    """)

    conn.commit()
