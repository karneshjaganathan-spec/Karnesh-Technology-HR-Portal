import sqlite3

DATABASE = "hr_portal.db"


class NotificationService:

    @staticmethod
    def get_connection():

        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row

        return conn


    # ==========================================
    # Get All Notifications
    # ==========================================

    @staticmethod
    def get_all():

        conn = NotificationService.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        SELECT *

        FROM notifications

        ORDER BY created_at DESC

        """)

        notifications = [

            dict(row)

            for row in cursor.fetchall()

        ]

        conn.close()

        return notifications


    # ==========================================
    # Get Notification
    # ==========================================

    @staticmethod
    def get(notification_id):

        conn = NotificationService.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        SELECT *

        FROM notifications

        WHERE notification_id=?

        """, (notification_id,))

        row = cursor.fetchone()

        conn.close()

        if row:

            return dict(row)

        return None


    # ==========================================
    # Add Notification
    # ==========================================

    @staticmethod
    def add(data):

        conn = NotificationService.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        INSERT INTO notifications(

            title,

            message,

            notification_type,

            recipient_type,

            recipient_id

        )

        VALUES(

        ?,?,?,?,?

        )

        """, (

            data["title"],

            data["message"],

            data["notification_type"],

            data["recipient_type"],

            data.get("recipient_id")

        ))

        conn.commit()

        notification_id = cursor.lastrowid

        conn.close()

        return notification_id


    # ==========================================
    # Mark Read
    # ==========================================

    @staticmethod
    def mark_read(notification_id):

        conn = NotificationService.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        UPDATE notifications

        SET is_read=1

        WHERE notification_id=?

        """, (notification_id,))

        conn.commit()

        conn.close()

        return True


    # ==========================================
    # Delete Notification
    # ==========================================

    @staticmethod
    def delete(notification_id):

        conn = NotificationService.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        DELETE

        FROM notifications

        WHERE notification_id=?

        """, (notification_id,))

        conn.commit()

        conn.close()

        return True