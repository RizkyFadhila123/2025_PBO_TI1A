import sqlite3
from konfigurasi import DB_PATH

def execute_query(query, params=()):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print("SQL Error:", e)
        return None
    finally:
        conn.close()

def fetch_query(query, params=(), fetch_one=False):
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchone() if fetch_one else cursor.fetchall()
    except Exception as e:
        print("SQL Error:", e)
        return None
    finally:
        conn.close()
