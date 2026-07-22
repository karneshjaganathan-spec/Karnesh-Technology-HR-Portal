import sqlite3

DATABASE = "hr_portal.db"


class ProfileService:

    @staticmethod
    def get_connection():
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn

    # ==========================================
    # Get Profile
    # ==========================================

    @staticmethod
    def get_profile(user_id):

        conn = ProfileService.get_connection()
        cursor = conn.cursor()

        cursor.execute("""

        SELECT

            u.user_id,
            u.username,
            r.role_name,

            e.employee_id,
            e.employee_code,
            e.first_name,
            e.last_name,
            e.gender,
            e.dob,
            e.email,
            e.phone,
            e.address,
            e.designation,
            e.salary,
            e.joining_date,
            e.status,

            d.department_name

        FROM users u

        LEFT JOIN employees e
        ON u.user_id=e.user_id

        LEFT JOIN roles r
        ON u.role_id=r.role_id

        LEFT JOIN departments d
        ON e.department_id=d.department_id

        WHERE u.user_id=?

        """, (user_id,))

        profile = cursor.fetchone()

        conn.close()

        if profile:
            return dict(profile)

        return None

    # ==========================================
    # Update Profile
    # ==========================================

    @staticmethod
    def update_profile(user_id, data):

        conn = ProfileService.get_connection()
        cursor = conn.cursor()

        cursor.execute("""

        UPDATE employees

        SET

            email=?,
            phone=?,
            address=?

        WHERE user_id=?

        """, (

            data["email"],
            data["phone"],
            data["address"],
            user_id

        ))

        conn.commit()
        conn.close()

        return True

    # ==========================================
    # Change Password
    # ==========================================

    @staticmethod
    def change_password(user_id, password):

        conn = ProfileService.get_connection()
        cursor = conn.cursor()

        cursor.execute("""

        UPDATE users

        SET password=?

        WHERE user_id=?

        """, (

            password,
            user_id

        ))

        conn.commit()
        conn.close()

        return True