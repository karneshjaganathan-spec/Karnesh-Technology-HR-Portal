import sqlite3
from config import DATABASE


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():

    conn = get_connection()

    cursor = conn.cursor()

    # -------------------------
    # Roles
    # -------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS roles(

            role_id INTEGER PRIMARY KEY AUTOINCREMENT,

            role_name TEXT UNIQUE NOT NULL

        )
    """)

    # -------------------------
    # Departments
    # -------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS departments(

            department_id INTEGER PRIMARY KEY AUTOINCREMENT,

            department_name TEXT NOT NULL,

            description TEXT

        )
    """)

    # -------------------------
    # Users
    # -------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(

            user_id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL,

            role_id INTEGER,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(role_id)

            REFERENCES roles(role_id)

        )
    """)

    # -------------------------
    # Employees
    # -------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees(

            employee_id INTEGER PRIMARY KEY AUTOINCREMENT,

            employee_code TEXT UNIQUE,

            first_name TEXT,

            last_name TEXT,

            gender TEXT,

            dob TEXT,

            email TEXT UNIQUE,

            phone TEXT,

            address TEXT,

            designation TEXT,

            salary REAL,

            joining_date TEXT,

            department_id INTEGER,

            user_id INTEGER,

            status TEXT DEFAULT 'Active',

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(department_id)

            REFERENCES departments(department_id),

            FOREIGN KEY(user_id)

            REFERENCES users(user_id)

        )
    """)

    # -------------------------
    # Attendance
    # -------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance(

            attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,

            employee_id INTEGER,

            attendance_date TEXT,

            check_in TEXT,

            check_out TEXT,

            status TEXT,

            FOREIGN KEY(employee_id)

            REFERENCES employees(employee_id)

        )
    """)

    # -------------------------
    # Leave Requests
    # -------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leave_requests(

            leave_id INTEGER PRIMARY KEY AUTOINCREMENT,

            employee_id INTEGER,

            leave_type TEXT,

            start_date TEXT,

            end_date TEXT,

            reason TEXT,

            status TEXT DEFAULT 'Pending',

            applied_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(employee_id)

            REFERENCES employees(employee_id)

        )
    """)

    # ==========================================
    # Default Data
    # ==========================================

    cursor.execute("SELECT COUNT(*) FROM roles")

    if cursor.fetchone()[0] == 0:

        cursor.executemany(

            "INSERT INTO roles(role_name) VALUES(?)",

            [

                ("Admin",),

                ("HR",),

                ("Employee",)

            ]

        )

    cursor.execute("SELECT COUNT(*) FROM departments")

    if cursor.fetchone()[0] == 0:

        cursor.executemany(

            """

            INSERT INTO departments(

            department_name,

            description

            )

            VALUES(?,?)

            """,

            [

                ("Human Resources","Recruitment"),

                ("Information Technology","Software Development"),

                ("Finance","Finance Department"),

                ("Marketing","Marketing Team"),

                ("Operations","Operations Team")

            ]

        )

    cursor.execute("SELECT COUNT(*) FROM users")

    if cursor.fetchone()[0] == 0:

        cursor.execute("""

            INSERT INTO users(

            username,

            password,

            role_id

            )

            VALUES(

            ?,?,?

            )

        """,

        (

            "admin",

            "admin123",

            1

        ))

    conn.commit()

    conn.close()