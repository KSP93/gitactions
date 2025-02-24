import os
import psycopg2
import pytest

@pytest.mark.database
def test_database_connection():
    """Test database connection using environment variables."""
    
    # Fetch database credentials from environment variables
    DB_HOST = os.getenv("DB_HOST", "3.94.10.52")
    DB_NAME = os.getenv("DB_NAME", "Orders")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASS = os.getenv("DB_PASS", "Blockhouse")
    DB_PORT = os.getenv("DB_PORT", "5432")

    try:
        # Attempt to establish a database connection
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT
        )
        conn.close()  # Close connection after successful test
        assert True  # Test passes if connection is successful
    except psycopg2.OperationalError as e:
        pytest.fail(f"Database connection failed: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error: {e}")
