import sqlite3


def create_database():
    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS menu (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        food_name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT NOT NULL,
        food_name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        total_price REAL NOT NULL
    )
    """)

    conn.commit()
    conn.close()

    print("Database Created Successfully!")