"""
This script creates a database, adds a "students" table to it, and inserts 50 records in the table
"""

import os
import psycopg2
from faker import Faker

DB_NAME = os.environ.get("PGDATABASE", "school")
DB_USER = os.environ.get("PGUSER", "postgres")
DB_PASS = os.environ.get("PGPASSWORD", "")
DB_HOST = os.environ.get("PGHOST", "localhost")
DB_PORT = os.environ.get("PGPORT", "5432")

# creation d'une connexion

conn = psycopg2.connect(
    database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
)
cur = conn.cursor()

# init un generateur
fake = Faker()

with conn:
    # drop table if it exists
    cur.execute("""DROP TABLE IF EXISTS Students CASCADE""")

    # create students table
    cur.execute(
        """CREATE TABLE Students (
                        id SERIAL PRIMARY KEY,
                        first_name VARCHAR(50),
                        last_name VARCHAR(50),
                        date_of_birth DATE,
                        address VARCHAR(100))"""
    )

    for _ in range(50):
        first_name = fake.first_name()
        last_name = fake.last_name()
        date_of_birth = fake.date_of_birth(None, 16, 35)
        # first_name = "John"
        # last_name = "Doe"
        # date_of_birth = date(2025, 3, 1)
        address = fake.address()[:100]

        # student_id
        cur.execute("""SELECT COALESCE(max(id), 0) FROM students""")
        student_id = cur.fetchall()
        student_id_generate = student_id[0][0] + 1

        cur.execute(
            "INSERT INTO students VALUES (%s, %s, %s ,%s, %s)",
            (student_id_generate, first_name, last_name, date_of_birth, address),
        )

print("Insert Done!")
