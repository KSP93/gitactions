import os
import psycopg2

def test_database_connection():
    DB_HOST = os.getenv("DB_HOST", "3.94.10.52")
    DB_NAME = os.getenv("DB_NAME", "Orders")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASS = os.getenv("DB_PASS", "Blockhouse")
    DB_PORT = os.getenv("DB_PORT", "5432")

    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT
        )
        conn.close()
        assert True
    except Exception:
        assert False, "Database connection failed"
