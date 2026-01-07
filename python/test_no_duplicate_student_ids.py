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
        dbname=os.getenv("PGDATABASE", "school"),
        user=os.getenv("PGUSER", "postgres"),
        password=os.getenv("PGPASSWORD", ""),
        host=os.getenv("PGHOST", "localhost"),
        port=os.getenv("PGPORT", "5432"),
    )
    yield conn
    conn.close()


def test_no_duplicate_student_ids(db_connection):
    """
    Test that 'student_id' in the 'students' table has no duplicate values.
    """
    with db_connection.cursor() as cur:
        cur.execute("""
            SELECT student_id, COUNT(*)
            FROM students
            GROUP BY student_id
            HAVING COUNT(*) > 1;
        """)
        duplicates = cur.fetchall()

    assert len(duplicates) == 0, f"Found duplicate student_ids: {duplicates}"
