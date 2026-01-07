import os
import psycopg2
import pytest


@pytest.fixture(scope="module")
def db_connection():
    """
    Creates a PostgreSQL database connection using environment variables.
    Closes automatically after the test module finishes.
    """
    conn = psycopg2.connect(
        dbname=os.environ.get("PGDATABASE", "school"),
        user=os.environ.get("PGUSER", "postgres"),
        password=os.environ.get("PGPASSWORD", ""),
        host=os.environ.get("PGHOST", "localhost"),
        port=os.environ.get("PGPORT", "5432"),
    )
    yield conn
    conn.close()


def test_no_duplicate_student_ids(db_connection):
    """
    Test that 'student_id' in the 'students' table has no duplicate values.
    """
    with db_connection.cursor() as cur:
        cur.execute("""
            SELECT id, COUNT(*)
            FROM students
            GROUP BY id
            HAVING COUNT(*) > 1;
        """)
        duplicates = cur.fetchall()

    assert len(duplicates) == 0, f"Found duplicate student_ids: {duplicates}"
