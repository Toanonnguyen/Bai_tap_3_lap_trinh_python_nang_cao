from psycopg2 import sql

def create_table(conn):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS students (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        age INTEGER NOT NULL,
        gender VARCHAR(10) NOT NULL,
        major VARCHAR(100) NOT NULL
    );
    """
    cur = conn.cursor()
    cur.execute(create_table_query)
    conn.commit()

def get_students(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    return rows

def add_student(conn, name, age, gender, major):
    cur = conn.cursor()
    cur.execute("INSERT INTO students (name, age, gender, major) VALUES (%s, %s, %s, %s)", (name, age, gender, major))
    conn.commit()

def update_student(conn, student_id, name, age, gender, major):
    cur = conn.cursor()
    cur.execute("UPDATE students SET name=%s, age=%s, gender=%s, major=%s WHERE id=%s", (name, age, gender, major, student_id))
    conn.commit()

def delete_student(conn, student_id):
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id=%s", (student_id,))
    conn.commit()
    reset_id_sequence(conn)

def reset_id_sequence(conn):
    cur = conn.cursor()
    cur.execute("SELECT setval(pg_get_serial_sequence('students', 'id'), COALESCE(MAX(id), 1)) FROM students")
    conn.commit()

def get_student_by_id(conn, student_id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM students WHERE id=%s", (student_id,))
    student = cur.fetchone()
    return student

def search_students(conn, search_term):
    cur = conn.cursor()
    search_query = sql.SQL("SELECT * FROM students WHERE name ILIKE %s OR CAST(age AS TEXT) ILIKE %s OR gender ILIKE %s OR major ILIKE %s")
    search_pattern = f"%{search_term}%"
    cur.execute(search_query, (search_pattern, search_pattern, search_pattern, search_pattern))
    rows = cur.fetchall()
    return rows
