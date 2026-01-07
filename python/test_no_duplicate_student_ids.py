"""
This script tests if the student table doesn't contain duplicate records
"""

import os
import psycopg2
import pytest


@pytest.fixture(name="db_connection")
def fixture_db_connection():
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
    Test that the 'students' table has no duplicate values
    """
    with db_connection.cursor() as cur:
        cur.execute(
            """
            SELECT first_name, last_name, date_of_birth, COUNT(*)
            FROM students
            GROUP BY 1,2,3
            HAVING COUNT(*) > 1;
        """
        )
        duplicates = cur.fetchall()

    assert len(duplicates) == 0, f"Found duplicate students: {duplicates}"
