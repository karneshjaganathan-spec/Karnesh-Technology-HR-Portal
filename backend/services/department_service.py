import sqlite3

DATABASE = "hr_portal.db"


class DepartmentService:

    @staticmethod
    def get_connection():
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn

    # =====================================
    # Get All Departments
    # =====================================
    @staticmethod
    def get_all():

        conn = DepartmentService.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                department_id,
                department_name,
                description
            FROM departments
            ORDER BY department_name ASC
        """)

        departments = [dict(row) for row in cursor.fetchall()]

        conn.close()

        return departments

    # =====================================
    # Get Department By ID
    # =====================================
    @staticmethod
    def get_by_id(department_id):

        conn = DepartmentService.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM departments
            WHERE department_id = ?
        """, (department_id,))

        department = cursor.fetchone()

        conn.close()

        if department:
            return dict(department)

        return None

    # =====================================
    # Add Department
    # =====================================
    @staticmethod
    def add(data):

        conn = DepartmentService.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO departments
            (
                department_name,
                description
            )
            VALUES (?, ?)
        """, (
            data["department_name"],
            data["description"]
        ))

        conn.commit()

        department_id = cursor.lastrowid

        conn.close()

        return department_id

    # =====================================
    # Update Department
    # =====================================
    @staticmethod
    def update(department_id, data):

        conn = DepartmentService.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE departments
            SET
                department_name = ?,
                description = ?
            WHERE department_id = ?
        """, (
            data["department_name"],
            data["description"],
            department_id
        ))

        conn.commit()
        conn.close()

        return True

    # =====================================
    # Delete Department
    # =====================================
    @staticmethod
    def delete(department_id):

        conn = DepartmentService.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM departments
            WHERE department_id = ?
        """, (department_id,))

        conn.commit()
        conn.close()

        return True