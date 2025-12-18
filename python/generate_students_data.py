import psycopg2
from faker import Faker

DB_NAME = "school"
DB_USER = "postgres"
DB_PASS = ""
DB_HOST = "localhost"
DB_PORT = 5432

# creation d'une connexion

conn = psycopg2.connect(database=DB_NAME,
                        user=DB_USER,
                        password=DB_PASS,
                        host=DB_HOST,
                        port=DB_PORT)
cur = conn.cursor()

# init un generateur
fake = Faker()

with conn:
    for _ in range(50):
        first_name = fake.first_name()
        last_name = fake.last_name()
        date_of_birth  = fake.date_of_birth(None,16,35)
        address  = fake.address()[:100]

        # student_id
        cur.execute("""SELECT max(student_id) FROM students""")       
        student_id = cur.fetchall()
        student_id_generate = student_id[0][0] + 1
        
        cur.execute("INSERT INTO students VALUES (%s, %s, %s ,%s, %s)", (student_id_generate, first_name
                                ,last_name, date_of_birth, address) )

print("Insert Done!")