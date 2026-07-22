import sqlite3

DATABASE = "hr_portal.db"


class SettingsService:

    @staticmethod
    def get_connection():

        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row

        return conn


    # =====================================
    # Get Settings
    # =====================================

    @staticmethod
    def get():

        conn = SettingsService.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        SELECT *

        FROM settings

        LIMIT 1

        """)

        row = cursor.fetchone()

        conn.close()

        if row:

            return dict(row)

        return None


    # =====================================
    # Update Settings
    # =====================================

    @staticmethod
    def update(data):

        conn = SettingsService.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        UPDATE settings

        SET

        company_name=?,

        company_email=?,

        company_phone=?,

        company_address=?,

        company_website=?,

        working_hours_start=?,

        working_hours_end=?,

        leave_per_year=?,

        currency=?,

        timezone=?,

        updated_at=CURRENT_TIMESTAMP

        """,(

            data["company_name"],

            data["company_email"],

            data["company_phone"],

            data["company_address"],

            data["company_website"],

            data["working_hours_start"],

            data["working_hours_end"],

            data["leave_per_year"],

            data["currency"],

            data["timezone"]

        ))

        conn.commit()

        conn.close()

        return True