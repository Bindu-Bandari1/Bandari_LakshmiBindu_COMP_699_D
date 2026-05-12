import sqlite3
import os

# -----------------------------
# DATABASE PATH
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "app.db")


# -----------------------------
# GET CONNECTION
# -----------------------------
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # dict-like rows
    return conn


# -----------------------------
# INIT DATABASE (RUN ONCE)
# -----------------------------
def init_db():
    if database_exists():
        print("Database already exists")
        return

    conn = get_connection()
    cursor = conn.cursor()

    schema_path = os.path.join(BASE_DIR, "schema.sql")

    if not os.path.exists(schema_path):
        raise FileNotFoundError("schema.sql not found")

    with open(schema_path, "r") as f:
        schema_sql = f.read()

    cursor.executescript(schema_sql)

    conn.commit()
    conn.close()

    print("Database initialized successfully")


# -----------------------------
# EXECUTE (INSERT / UPDATE / DELETE)
# -----------------------------
def execute_query(query, params=()):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query, params)
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print("Database error:", e)
        return None
    finally:
        conn.close()


# -----------------------------
# FETCH ONE
# -----------------------------
def fetch_one(query, params=()):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query, params)
        return cursor.fetchone()
    except Exception as e:
        print("Fetch one error:", e)
        return None
    finally:
        conn.close()


# -----------------------------
# FETCH ALL
# -----------------------------
def fetch_all(query, params=()):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query, params)
        return cursor.fetchall()
    except Exception as e:
        print("Fetch all error:", e)
        return []
    finally:
        conn.close()


# -----------------------------
# EXECUTE + FETCH (SELECT ONLY)
# -----------------------------
def execute_and_fetch(query, params=()):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query, params)
        return cursor.fetchall()
    except Exception as e:
        print("Execute fetch error:", e)
        return []
    finally:
        conn.close()


# -----------------------------
# CHECK DB EXISTS
# -----------------------------
def database_exists():
    return os.path.exists(DB_PATH)