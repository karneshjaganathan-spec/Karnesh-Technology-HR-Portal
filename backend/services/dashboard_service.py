import sqlite3

DATABASE = "hr_portal.db"


class DashboardService:

    @staticmethod
    def get_connection():
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def get_dashboard_stats():

        conn = DashboardService.get_connection()
        cursor = conn.cursor()

        # Total Employees
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM employees
        """)
        total_employees = cursor.fetchone()["total"]

        # Active Employees
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM employees
            WHERE status='Active'
        """)
        active_employees = cursor.fetchone()["total"]

        # Total Departments
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM departments
        """)
        total_departments = cursor.fetchone()["total"]

        # Pending Leave Requests
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM leave_requests
            WHERE status='Pending'
        """)
        pending_leaves = cursor.fetchone()["total"]

        # Today's Attendance
        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM attendance
            WHERE attendance_date = DATE('now')
        """)
        today_attendance = cursor.fetchone()["total"]

        conn.close()

        return {
            "total_employees": total_employees,
            "active_employees": active_employees,
            "total_departments": total_departments,
            "pending_leaves": pending_leaves,
            "today_attendance": today_attendance
        }

    @staticmethod
    def recent_employees(limit=5):

        conn = DashboardService.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                employee_code,
                first_name,
                last_name,
                designation,
                joining_date,
                status
            FROM employees
            ORDER BY employee_id DESC
            LIMIT ?
        """, (limit,))

        employees = [dict(row) for row in cursor.fetchall()]

        conn.close()

        return employees

    @staticmethod
    def department_summary():

        conn = DashboardService.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                d.department_name,
                COUNT(e.employee_id) AS employee_count
            FROM departments d
            LEFT JOIN employees e
            ON d.department_id = e.department_id
            GROUP BY d.department_id
            ORDER BY d.department_name
        """)

        summary = [dict(row) for row in cursor.fetchall()]

        conn.close()

        return summary