import sqlite3

DATABASE = "hr_portal.db"


class AttendanceService:

    @staticmethod
    def get_connection():
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn

    # ======================================
    # Get All Attendance
    # ======================================

    @staticmethod
    def get_all():

        conn = AttendanceService.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                a.attendance_id,
                a.employee_id,
                e.employee_code,
                e.first_name,
                e.last_name,
                a.attendance_date,
                a.check_in,
                a.check_out,
                a.status
            FROM attendance a
            JOIN employees e
            ON a.employee_id = e.employee_id
            ORDER BY a.attendance_date DESC
        """)

        attendance = [dict(row) for row in cursor.fetchall()]

        conn.close()

        return attendance

    # ======================================
    # Get Attendance By ID
    # ======================================

    @staticmethod
    def get_by_id(attendance_id):

        conn = AttendanceService.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM attendance
            WHERE attendance_id = ?
        """, (attendance_id,))

        row = cursor.fetchone()

        conn.close()

        if row:
            return dict(row)

        return None

    # ======================================
    # Mark Attendance
    # ======================================

    @staticmethod
    def add(data):

        conn = AttendanceService.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO attendance
            (
                employee_id,
                attendance_date,
                check_in,
                check_out,
                status
            )
            VALUES (?, ?, ?, ?, ?)
        """, (

            data["employee_id"],
            data["attendance_date"],
            data["check_in"],
            data["check_out"],
            data["status"]

        ))

        conn.commit()

        attendance_id = cursor.lastrowid

        conn.close()

        return attendance_id

    # ======================================
    # Update Attendance
    # ======================================

    @staticmethod
    def update(attendance_id, data):

        conn = AttendanceService.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE attendance
            SET
                employee_id = ?,
                attendance_date = ?,
                check_in = ?,
                check_out = ?,
                status = ?
            WHERE attendance_id = ?
        """, (

            data["employee_id"],
            data["attendance_date"],
            data["check_in"],
            data["check_out"],
            data["status"],
            attendance_id

        ))

        conn.commit()
        conn.close()

        return True

    # ======================================
    # Delete Attendance
    # ======================================

    @staticmethod
    def delete(attendance_id):

        conn = AttendanceService.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM attendance
            WHERE attendance_id = ?
        """, (attendance_id,))

        conn.commit()
        conn.close()

        return True

    # ======================================
    # Today's Attendance Count
    # ======================================

    @staticmethod
    def today_count():

        conn = AttendanceService.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM attendance
            WHERE attendance_date = DATE('now')
        """)

        total = cursor.fetchone()["total"]

        conn.close()

        return total

    # ======================================
    # Attendance By Employee
    # ======================================

    @staticmethod
    def employee_history(employee_id):

        conn = AttendanceService.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM attendance
            WHERE employee_id = ?
            ORDER BY attendance_date DESC
        """, (employee_id,))

        history = [dict(row) for row in cursor.fetchall()]

        conn.close()

        return history

    # ======================================
    # Search Attendance
    # ======================================

    @staticmethod
    def search(date):

        conn = AttendanceService.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                a.attendance_id,
                e.employee_code,
                e.first_name,
                e.last_name,
                a.attendance_date,
                a.check_in,
                a.check_out,
                a.status
            FROM attendance a
            JOIN employees e
            ON a.employee_id = e.employee_id
            WHERE attendance_date = ?
        """, (date,))

        attendance = [dict(row) for row in cursor.fetchall()]

        conn.close()

        return attendance