import sqlite3

DATABASE = "hr_portal.db"


class PermissionService:

    @staticmethod
    def get_connection():

        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row

        return conn


    # ===========================
    # Get All Permissions
    # ===========================

    @staticmethod
    def get_permissions():

        conn = PermissionService.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        SELECT *

        FROM permissions

        ORDER BY module_name

        """)

        permissions = [

            dict(row)

            for row in cursor.fetchall()

        ]

        conn.close()

        return permissions


    # ===========================
    # Get Role Permissions
    # ===========================

    @staticmethod
    def get_role_permissions(role_id):

        conn = PermissionService.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        SELECT permission_id

        FROM role_permissions

        WHERE role_id=?

        """, (role_id,))

        permissions = [

            row["permission_id"]

            for row in cursor.fetchall()

        ]

        conn.close()

        return permissions


    # ===========================
    # Update Role Permissions
    # ===========================

    @staticmethod
    def update_permissions(role_id, permission_ids):

        conn = PermissionService.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        DELETE FROM role_permissions

        WHERE role_id=?

        """, (role_id,))

        for permission in permission_ids:

            cursor.execute("""

            INSERT INTO role_permissions(

                role_id,

                permission_id

            )

            VALUES(?,?)

            """, (

                role_id,

                permission

            ))

        conn.commit()

        conn.close()

        return True