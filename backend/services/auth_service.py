import sqlite3

DATABASE = "hr_portal.db"


class AuthService:

    @staticmethod
    def get_connection():
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def login(username, password):

        conn = AuthService.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                user_id,
                username,
                password,
                role_id
            FROM users
            WHERE username = ?
        """, (username,))

        user = cursor.fetchone()

        conn.close()

        if user is None:
            return None

        # Plain text password check
        if user["password"] != password:
            return None

        return {
            "id": user["user_id"],
            "username": user["username"],
            "role_id": user["role_id"]
        }