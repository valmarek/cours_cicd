-- database : school
--- 1) Ouvrir PgAdmin
--- 2) Databases -> Create -> Database
--- 3) database name : school
--- Create table in public schemas

DROP TABLE IF EXISTS Students CASCADE;

-- Table 1: Students
CREATE TABLE Students (
    student_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    date_of_birth DATE,
    address VARCHAR(100)
);