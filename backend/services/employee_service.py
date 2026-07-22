import sqlite3

DATABASE = "hr_portal.db"


class EmployeeService:

    @staticmethod
    def get_connection():

        conn = sqlite3.connect(DATABASE, timeout=30)
        conn.row_factory = sqlite3.Row

        return conn

    # ==========================================
    # Get All Employees
    # ==========================================

    @staticmethod
    def get_all():

        conn = EmployeeService.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        SELECT

            e.*,

            d.department_name

        FROM employees e

        LEFT JOIN departments d

        ON e.department_id = d.department_id

        ORDER BY e.employee_id DESC

        """)

        employees = [

            dict(row)

            for row in cursor.fetchall()

        ]

        conn.close()

        return employees

    # ==========================================
    # Get Employee By ID
    # ==========================================

    @staticmethod
    def get_by_id(employee_id):

        conn = EmployeeService.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        SELECT

            e.*,

            d.department_name

        FROM employees e

        LEFT JOIN departments d

        ON e.department_id = d.department_id

        WHERE e.employee_id=?

        """, (employee_id,))

        row = cursor.fetchone()

        conn.close()

        if row:

            return dict(row)

        return None

    # ==========================================
    # Add Employee
    # ==========================================

    @staticmethod
    def add(data):

        conn = EmployeeService.get_connection()

        try:

            cursor = conn.cursor()

            cursor.execute("""

            INSERT INTO employees(

                employee_code,

                first_name,

                last_name,

                gender,

                dob,

                email,

                phone,

                address,

                designation,

                salary,

                joining_date,

                department_id,

                user_id,

                status

            )

            VALUES(

                ?,?,?,?,?,?,?,?,?,?,?,?,?,?

            )

            """, (

                data["employee_code"],
                data["first_name"],
                data["last_name"],
                data["gender"],
                data["dob"],
                data["email"],
                data["phone"],
                data["address"],
                data["designation"],
                data["salary"],
                data["joining_date"],
                data["department_id"],
                data["user_id"],
                data["status"]

            ))

            conn.commit()

            return cursor.lastrowid

        finally:

            conn.close()

    # ==========================================
    # Delete Employee
    # ==========================================

    @staticmethod
    def delete(employee_id):

        conn = EmployeeService.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        DELETE

        FROM employees

        WHERE employee_id=?

        """, (employee_id,))

        conn.commit()

        conn.close()

        return True

    # ==========================================
    # Search Employee
    # ==========================================

    @staticmethod
    def search(keyword):

        conn = EmployeeService.get_connection()

        cursor = conn.cursor()

        keyword = f"%{keyword}%"

        cursor.execute("""

        SELECT

            e.*,

            d.department_name

        FROM employees e

        LEFT JOIN departments d

        ON e.department_id = d.department_id

        WHERE

            e.employee_code LIKE ?

            OR e.first_name LIKE ?

            OR e.last_name LIKE ?

            OR e.email LIKE ?

            OR d.department_name LIKE ?

        ORDER BY e.employee_id DESC

        """, (

            keyword,

            keyword,

            keyword,

            keyword,

            keyword

        ))

        employees = [

            dict(row)

            for row in cursor.fetchall()

        ]

        conn.close()

        return employees

    # ==========================================
    # Total Employees
    # ==========================================

    @staticmethod
    def count():

        conn = EmployeeService.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        SELECT COUNT(*)

        FROM employees

        """)

        total = cursor.fetchone()[0]

        conn.close()

        return total

    # ==========================================
    # Active Employees
    # ==========================================

    @staticmethod
    def active_count():

        conn = EmployeeService.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        SELECT COUNT(*)

        FROM employees

        WHERE status='Active'

        """)

        total = cursor.fetchone()[0]

        conn.close()

        return total
    # ======================================
    # Check Employee Exists
    # ======================================
    @staticmethod
    def employee_exists(employee_code, user_id):

        conn = EmployeeService.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT employee_code, user_id
            FROM employees
            WHERE employee_code = ?
            OR user_id = ?
        """, (employee_code, user_id))

        employee = cursor.fetchone()

        conn.close()

        if employee:
            return dict(employee)

        return None
    