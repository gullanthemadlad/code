import os
import psycopg2
from dotenv import load_dotenv

load_dotenv(override=True)

DATABASE_NAME = os.getenv("DATABASE")
PASSWORD = os.getenv("PASSWORD")

# This function should create a connection
def get_connection():
    return psycopg2.connect(
        dbname=DATABASE_NAME,
        user="postgres",  # change if needed
        password=PASSWORD,
        host="localhost",  # change if needed
        port="1111",  # change if needed
    )


def create_tables():
    con = get_connection()
    create_tables_query = """
    CREATE TABLE IF NOT EXISTS Departments (
        department_id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        location TEXT
    );
    
    CREATE TABLE IF NOT EXISTS Students (
        student_id SERIAL PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        birthdate DATE
    );
    
    CREATE TABLE IF NOT EXISTS Instructors (
        instructor_id SERIAL PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        department_id INTEGER REFERENCES Departments(department_id)
    );
    
    CREATE TABLE IF NOT EXISTS Courses (
        course_id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        credits INTEGER NOT NULL,
        department_id INTEGER REFERENCES Departments(department_id)
    );
    
    CREATE TABLE IF NOT EXISTS Enrollments (
        enrollment_id SERIAL PRIMARY KEY,
        student_id INTEGER REFERENCES Students(student_id),
        course_id INTEGER REFERENCES Courses(course_id),
        enrollment_date DATE,
        grade TEXT,
        UNIQUE(student_id, course_id)
    );
    """

    with con:
        with con.cursor() as cursor:
            cursor.execute(create_tables_query)
            print("Tables created successfully.")


if __name__ == "__main__":
    # Only reason to execute this file would be to create new tables, meaning it serves a migration file
    create_tables()

