import sqlite3

DATABASE = "hr_portal.db"


class ReportService:

    @staticmethod
    def get_connection():
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn

    # ==========================================
    # Dashboard Summary
    # ==========================================

    @staticmethod
    def dashboard_summary():

        conn = ReportService.get_connection()
        cursor = conn.cursor()

        # Employees
        cursor.execute("SELECT COUNT(*) AS total FROM employees")
        employees = cursor.fetchone()["total"]

        # Departments
        cursor.execute("SELECT COUNT(*) AS total FROM departments")
        departments = cursor.fetchone()["total"]

        # Attendance Today
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM attendance
            WHERE attendance_date = DATE('now')
        """)
        attendance = cursor.fetchone()["total"]

        # Pending Leaves
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM leave_requests
            WHERE status='Pending'
        """)
        pending = cursor.fetchone()["total"]

        conn.close()

        return {
            "employees": employees,
            "departments": departments,
            "attendance": attendance,
            "pending_leaves": pending
        }

    # ==========================================
    # Department Report
    # ==========================================

    @staticmethod
    def department_report():

        conn = ReportService.get_connection()
        cursor = conn.cursor()

        cursor.execute("""

        SELECT

            d.department_name,

            COUNT(e.employee_id) employee_count

        FROM departments d

        LEFT JOIN employees e

        ON d.department_id=e.department_id

        GROUP BY d.department_id

        ORDER BY d.department_name

        """)

        report = [dict(row) for row in cursor.fetchall()]

        conn.close()

        return report

    # ==========================================
    # Attendance Report
    # ==========================================

    @staticmethod
    def attendance_report():

        conn = ReportService.get_connection()
        cursor = conn.cursor()

        cursor.execute("""

        SELECT

            attendance_date,

            COUNT(*) total

        FROM attendance

        GROUP BY attendance_date

        ORDER BY attendance_date DESC

        """)

        report = [dict(row) for row in cursor.fetchall()]

        conn.close()

        return report

    # ==========================================
    # Leave Report
    # ==========================================

    @staticmethod
    def leave_report():

        conn = ReportService.get_connection()
        cursor = conn.cursor()

        cursor.execute("""

        SELECT

            status,

            COUNT(*) total

        FROM leave_requests

        GROUP BY status

        """)

        report = [dict(row) for row in cursor.fetchall()]

        conn.close()

        return report

    # ==========================================
    # Salary Report
    # ==========================================

    @staticmethod
    def salary_report():

        conn = ReportService.get_connection()
        cursor = conn.cursor()

        cursor.execute("""

        SELECT

            employee_code,

            first_name,

            last_name,

            designation,

            salary

        FROM employees

        ORDER BY salary DESC

        """)

        report = [dict(row) for row in cursor.fetchall()]

        conn.close()

        return report