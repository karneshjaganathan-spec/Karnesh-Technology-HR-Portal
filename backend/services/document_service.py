import sqlite3

DATABASE = "hr_portal.db"


class DocumentService:

    @staticmethod
    def get_connection():

        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row

        return conn


    # ==========================================
    # Get All Documents
    # ==========================================

    @staticmethod
    def get_all():

        conn = DocumentService.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        SELECT

            d.document_id,

            d.employee_id,

            e.employee_code,

            e.first_name,

            e.last_name,

            d.document_name,

            d.document_type,

            d.file_name,

            d.file_path,

            d.uploaded_on,

            d.remarks

        FROM documents d

        INNER JOIN employees e

        ON d.employee_id=e.employee_id

        ORDER BY d.uploaded_on DESC

        """)

        documents = [

            dict(row)

            for row in cursor.fetchall()

        ]

        conn.close()

        return documents


    # ==========================================
    # Get Single Document
    # ==========================================

    @staticmethod
    def get(document_id):

        conn = DocumentService.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        SELECT *

        FROM documents

        WHERE document_id=?

        """, (document_id,))

        document = cursor.fetchone()

        conn.close()

        if document:

            return dict(document)

        return None


    # ==========================================
    # Add Document
    # ==========================================

    @staticmethod
    def add(data):

        conn = DocumentService.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        INSERT INTO documents(

            employee_id,

            document_name,

            document_type,

            file_name,

            file_path,

            uploaded_by,

            remarks

        )

        VALUES(

        ?,?,?,?,?,?,?

        )

        """, (

            data["employee_id"],

            data["document_name"],

            data["document_type"],

            data["file_name"],

            data["file_path"],

            data["uploaded_by"],

            data["remarks"]

        ))

        conn.commit()

        document_id = cursor.lastrowid

        conn.close()

        return document_id


    # ==========================================
    # Delete Document
    # ==========================================

    @staticmethod
    def delete(document_id):

        conn = DocumentService.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        DELETE

        FROM documents

        WHERE document_id=?

        """, (document_id,))

        conn.commit()

        conn.close()

        return True