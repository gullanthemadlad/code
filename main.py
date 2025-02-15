from fastapi import FastAPI, HTTPException, Query
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os
from setup import get_connection
from pydantic import BaseModel
from typing import List, Optional

load_dotenv(override=True)

app = FastAPI()

class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    birthdate: str  

class InstructorCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    department_id: int

@app.get("/students")
def list_students():
    con = get_connection()
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM Students;")
            return cursor.fetchall()

@app.get("/students/{student_id}")
def get_student(student_id: int):
    con = get_connection()
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM Students WHERE student_id = %s;", (student_id,))
            student = cursor.fetchone()
            if not student:
                raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.get("/students/filter")
def search_students(name: str = Query(..., min_length=1)):
    con = get_connection()
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM Students WHERE first_name ILIKE %s OR last_name ILIKE %s;", 
                           (f"%{name}%", f"%{name}%"))
            return cursor.fetchall()

@app.get("/courses")
def list_courses():
    con = get_connection()
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM Courses;")
            return cursor.fetchall()

@app.get("/courses/{course_id}")
def get_course(course_id: int):
    con = get_connection()
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM Courses WHERE course_id = %s;", (course_id,))
            course = cursor.fetchone()
            if not course:
                raise HTTPException(status_code=404, detail="Course not found")
    return course

@app.get("/instructors")
def list_instructors():
    con = get_connection()
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM Instructors;")
            return cursor.fetchall()

@app.get("/instructors/{instructor_id}")
def get_instructor(instructor_id: int):
    con = get_connection()
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM Instructors WHERE instructor_id = %s;", (instructor_id,))
            instructor = cursor.fetchone()
            if not instructor:
                raise HTTPException(status_code=404, detail="Instructor not found")
    return instructor

@app.get("/enrollments")
def list_enrollments():
    con = get_connection()
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM Enrollments;")
            return cursor.fetchall()

@app.post("/students", status_code=201)
def add_student(student: StudentCreate):
    con = get_connection()
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "INSERT INTO Students (first_name, last_name, email, birthdate) VALUES (%s, %s, %s, %s) RETURNING *;",
                (student.first_name, student.last_name, student.email, student.birthdate)
            )
            return cursor.fetchone()

@app.post("/instructors", status_code=201)
def add_instructor(instructor: InstructorCreate):
    con = get_connection()
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "INSERT INTO Instructors (first_name, last_name, email, department_id) VALUES (%s, %s, %s, %s) RETURNING *;",
                (instructor.first_name, instructor.last_name, instructor.email, instructor.department_id)
            )
            return cursor.fetchone()

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    con = get_connection()
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("DELETE FROM Students WHERE student_id = %s RETURNING student_id;", (student_id,))
            deleted = cursor.fetchone()
            if not deleted:
                raise HTTPException(status_code=404, detail="Student not found")
    return {"message": f"Student with ID {student_id} deleted successfully."}

@app.delete("/courses/{course_id}")
def delete_course(course_id: int):
    con = get_connection()
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("DELETE FROM Courses WHERE course_id = %s RETURNING course_id;", (course_id,))
            deleted = cursor.fetchone()
            if not deleted:
                raise HTTPException(status_code=404, detail="Course not found")
    return {"message": f"Course with ID {course_id} deleted successfully."}

@app.delete("/instructors/{instructor_id}")
def delete_instructor(instructor_id: int):
    con = get_connection()
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("DELETE FROM Instructors WHERE instructor_id = %s RETURNING instructor_id;", (instructor_id,))
            deleted = cursor.fetchone()
            if not deleted:
                raise HTTPException(status_code=404, detail="Instructor not found")
    return {"message": f"Instructor with ID {instructor_id} deleted successfully."}
