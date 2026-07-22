import sqlite3

DATABASE = "hr_portal.db"


class LeaveService:

    @staticmethod
    def get_connection():
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn

    # ======================================
    # Get All Leave Requests
    # ======================================
    @staticmethod
    def get_all():

        conn = LeaveService.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                l.leave_id,
                l.employee_id,
                e.employee_code,
                e.first_name,
                e.last_name,
                l.leave_type,
                l.start_date,
                l.end_date,
                l.reason,
                l.status,
                l.applied_on
            FROM leave_requests l
            JOIN employees e
            ON l.employee_id = e.employee_id
            ORDER BY l.applied_on DESC
        """)

        leaves = [dict(row) for row in cursor.fetchall()]

        conn.close()

        return leaves

    # ======================================
    # Get Leave By ID
    # ======================================
    @staticmethod
    def get_by_id(leave_id):

        conn = LeaveService.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM leave_requests
            WHERE leave_id = ?
        """, (leave_id,))

        leave = cursor.fetchone()

        conn.close()

        if leave:
            return dict(leave)

        return None

    # ======================================
    # Apply Leave
    # ======================================
    @staticmethod
    def add(data):

        conn = LeaveService.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO leave_requests
            (
                employee_id,
                leave_type,
                start_date,
                end_date,
                reason,
                status,
                applied_on
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (

            data["employee_id"],
            data["leave_type"],
            data["start_date"],
            data["end_date"],
            data["reason"],
            data["status"],
            data["applied_on"]

        ))

        conn.commit()

        leave_id = cursor.lastrowid

        conn.close()

        return leave_id

    # ======================================
    # Update Leave
    # ======================================
    @staticmethod
    def update(leave_id, data):

        conn = LeaveService.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE leave_requests
            SET
                employee_id = ?,
                leave_type = ?,
                start_date = ?,
                end_date = ?,
                reason = ?,
                status = ?
            WHERE leave_id = ?
        """, (

            data["employee_id"],
            data["leave_type"],
            data["start_date"],
            data["end_date"],
            data["reason"],
            data["status"],
            leave_id

        ))

        conn.commit()
        conn.close()

        return True

    # ======================================
    # Delete Leave
    # ======================================
    @staticmethod
    def delete(leave_id):

        conn = LeaveService.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM leave_requests
            WHERE leave_id = ?
        """, (leave_id,))

        conn.commit()
        conn.close()

        return True

    # ======================================
    # Pending Leave Count
    # ======================================
    @staticmethod
    def pending_count():

        conn = LeaveService.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM leave_requests
            WHERE status='Pending'
        """)

        total = cursor.fetchone()["total"]

        conn.close()

        return total

    # ======================================
    # Leave History By Employee
    # ======================================
    @staticmethod
    def employee_history(employee_id):

        conn = LeaveService.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM leave_requests
            WHERE employee_id = ?
            ORDER BY applied_on DESC
        """, (employee_id,))

        history = [dict(row) for row in cursor.fetchall()]

        conn.close()

        return history

    # ======================================
    # Approve / Reject Leave
    # ======================================
    @staticmethod
    def change_status(leave_id, status):

        conn = LeaveService.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE leave_requests
            SET status = ?
            WHERE leave_id = ?
        """, (
            status,
            leave_id
        ))

        conn.commit()
        conn.close()

        return True

    # ======================================
    # Search Leave
    # ======================================
    @staticmethod
    def search(status):

        conn = LeaveService.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                l.leave_id,
                e.employee_code,
                e.first_name,
                e.last_name,
                l.leave_type,
                l.start_date,
                l.end_date,
                l.reason,
                l.status
            FROM leave_requests l
            JOIN employees e
            ON l.employee_id = e.employee_id
            WHERE l.status = ?
            ORDER BY l.applied_on DESC
        """, (status,))

        leaves = [dict(row) for row in cursor.fetchall()]

        conn.close()

        return leaves