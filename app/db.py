import os
import pymysql
from pymysql.cursors import DictCursor
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'emergency_dept'),
    'cursorclass': DictCursor,
}


def get_conn():
    return pymysql.connect(**DB_CONFIG)


def query(sql, params=None):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params or ())
            result = cur.fetchall()
        conn.commit()
        return result
    finally:
        conn.close()


def query_one(sql, params=None):
    rows = query(sql, params)
    return rows[0] if rows else None


def execute(sql, params=None):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params or ())
            affected = cur.rowcount
        conn.commit()
        return affected
    finally:
        conn.close()


def execute_last_id(sql, params=None):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params or ())
            last_id = cur.lastrowid
        conn.commit()
        return last_id
    finally:
        conn.close()
