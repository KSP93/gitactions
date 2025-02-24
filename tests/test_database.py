import os
import psycopg2
import pytest

@pytest.mark.database
def test_database_connection():
    """Test database connection with environment variables."""
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_NAME = os.getenv("DB_NAME", "orders_db")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASS = os.getenv("DB_PASS", "password")
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
    except Exception as e:
        pytest.fail(f"Database connection failed: {e}")
