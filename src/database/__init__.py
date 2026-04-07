import sqlite3 as sql

def create_database():
    connect = sql.connect("databases/dataBank.db")
    cursor = connect.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT,
            card_id INTEGER
                )
    """
    )
    connect.commit()
    connect.close()