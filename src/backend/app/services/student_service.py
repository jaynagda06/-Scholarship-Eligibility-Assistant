import sqlite3
from . import database as db

def list_students(limit=50, phone=None):
    conn = db.get_db()
    conditions = []
    params = []
    if phone:
        conditions.append("phone LIKE ?")
        params.append(f"%{phone}%")
    clause = "WHERE 1=1"
    if conditions:
        clause += " AND " + " AND ".join(conditions)
    sql = f"SELECT * FROM students {clause} ORDER BY created_at DESC LIMIT ?"
    params.append(limit)
    rows = conn.execute(sql, params).fetchall()
    return [dict(row) for row in rows]

def get_student(student_id):
    conn = db.get_db()
    row = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    return dict(row) if row else None

def create_student(data):
    conn = db.get_db()
    cur = conn.execute(
        "INSERT INTO students (phone, name, school, degree, year, annual_income, category, disability_pct, preferred_language) VALUES (?,?,?,?,?,?,?,?,?)",
        (data["phone"], data["name"], data.get("school",""), data.get("degree",""),
         data.get("year",0), data.get("annual_income",0.0), data.get("category",""),
         data.get("disability_pct",0), data.get("preferred_language","en"))
    )
    conn.commit()
    return cur.lastrowid

def seed_sample():
    conn = db.get_db()
    conn.execute("DELETE FROM students")
    conn.execute("""
        INSERT INTO students
        (phone, name, school, degree, year, annual_income, category, disability_pct)
        VALUES
        ('9876543210','Ravi Kumar','XYZ School','12th','2024',250000.00,'GENERAL',0),
        ('9876543211','Priya Patel','ABC College','BTECH_2','2024',300000.00,'GENERAL_GIRLS',0),
        ('9876543212','Anil Jeevan','Govt High School','10th','2024',150000.00,'SC',0),
        ('9876543213','Sunita Devi','Rural College','DIPLOMA_1','2024',240000.00,'SOCIAL_PWD',40)
    """)
    conn.commit()
    print("Seeded 4 students")
