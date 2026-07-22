import sqlite3

DATABASE = "hr_portal.db"


class AssetService:

    @staticmethod
    def get_connection():

        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row

        return conn


    # ==========================================
    # Get All Assets
    # ==========================================

    @staticmethod
    def get_all():

        conn = AssetService.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        SELECT

            a.*,

            e.employee_code,

            e.first_name,

            e.last_name

        FROM assets a

        LEFT JOIN employees e

        ON a.employee_id=e.employee_id

        ORDER BY a.created_at DESC

        """)

        assets = [

            dict(row)

            for row in cursor.fetchall()

        ]

        conn.close()

        return assets


    # ==========================================
    # Get Asset
    # ==========================================

    @staticmethod
    def get(asset_id):

        conn = AssetService.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        SELECT *

        FROM assets

        WHERE asset_id=?

        """, (asset_id,))

        asset = cursor.fetchone()

        conn.close()

        if asset:

            return dict(asset)

        return None


    # ==========================================
    # Add Asset
    # ==========================================

    @staticmethod
    def add(data):

        conn = AssetService.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        INSERT INTO assets(

            asset_code,

            asset_name,

            category,

            brand,

            model,

            serial_number,

            purchase_date,

            purchase_cost,

            warranty_expiry,

            status,

            employee_id,

            assigned_date,

            remarks

        )

        VALUES(

        ?,?,?,?,?,?,?,?,?,?,?,?,?

        )

        """, (

            data["asset_code"],

            data["asset_name"],

            data["category"],

            data["brand"],

            data["model"],

            data["serial_number"],

            data["purchase_date"],

            data["purchase_cost"],

            data["warranty_expiry"],

            data["status"],

            data.get("employee_id"),

            data.get("assigned_date"),

            data.get("remarks")

        ))

        conn.commit()

        asset_id = cursor.lastrowid

        conn.close()

        return asset_id


    # ==========================================
    # Update Asset
    # ==========================================

    @staticmethod
    def update(asset_id, data):

        conn = AssetService.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        UPDATE assets

        SET

            asset_name=?,

            category=?,

            brand=?,

            model=?,

            serial_number=?,

            purchase_date=?,

            purchase_cost=?,

            warranty_expiry=?,

            status=?,

            employee_id=?,

            assigned_date=?,

            returned_date=?,

            remarks=?

        WHERE asset_id=?

        """, (

            data["asset_name"],

            data["category"],

            data["brand"],

            data["model"],

            data["serial_number"],

            data["purchase_date"],

            data["purchase_cost"],

            data["warranty_expiry"],

            data["status"],

            data.get("employee_id"),

            data.get("assigned_date"),

            data.get("returned_date"),

            data.get("remarks"),

            asset_id

        ))

        conn.commit()

        conn.close()

        return True


    # ==========================================
    # Delete Asset
    # ==========================================

    @staticmethod
    def delete(asset_id):

        conn = AssetService.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        DELETE

        FROM assets

        WHERE asset_id=?

        """, (asset_id,))

        conn.commit()

        conn.close()

        return True


    # ==========================================
    # Dashboard Summary
    # ==========================================

    @staticmethod
    def summary():

        conn = AssetService.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        SELECT

            COUNT(*) total_assets,

            SUM(CASE WHEN status='Available' THEN 1 ELSE 0 END) available_assets,

            SUM(CASE WHEN status='Assigned' THEN 1 ELSE 0 END) assigned_assets,

            SUM(CASE WHEN status='Maintenance' THEN 1 ELSE 0 END) maintenance_assets

        FROM assets

        """)

        result = dict(cursor.fetchone())

        conn.close()

        return result