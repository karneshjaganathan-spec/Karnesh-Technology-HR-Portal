import sqlite3
from datetime import datetime

DATABASE = "hr_portal.db"


class PayrollService:

    @staticmethod
    def get_connection():
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn

    # ==========================================
    # Get All Payroll Records
    # ==========================================

    @staticmethod
    def get_all():

        conn = PayrollService.get_connection()
        cursor = conn.cursor()

        cursor.execute("""

        SELECT

            p.payroll_id,
            p.employee_id,
            e.employee_code,
            e.first_name,
            e.last_name,
            e.designation,

            p.basic_salary,
            p.allowances,
            p.deductions,
            p.net_salary,

            p.pay_month,
            p.payment_date,
            p.status

        FROM payroll p

        INNER JOIN employees e

        ON p.employee_id=e.employee_id

        ORDER BY p.payment_date DESC

        """)

        data = [dict(row) for row in cursor.fetchall()]

        conn.close()

        return data

    # ==========================================
    # Get Payroll By ID
    # ==========================================

    @staticmethod
    def get_by_id(payroll_id):

        conn = PayrollService.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        SELECT *

        FROM payroll

        WHERE payroll_id=?

        """, (payroll_id,))

        payroll = cursor.fetchone()

        conn.close()

        if payroll:

            return dict(payroll)

        return None

    # ==========================================
    # Generate Payroll
    # ==========================================

    @staticmethod
    def add(data):

        net_salary = (
            float(data["basic_salary"])
            + float(data["allowances"])
            - float(data["deductions"])
        )

        conn = PayrollService.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        INSERT INTO payroll(

            employee_id,
            basic_salary,
            allowances,
            deductions,
            net_salary,
            pay_month,
            payment_date,
            status

        )

        VALUES(?,?,?,?,?,?,?,?)

        """, (

            data["employee_id"],
            data["basic_salary"],
            data["allowances"],
            data["deductions"],
            net_salary,
            data["pay_month"],
            data["payment_date"],
            data["status"]

        ))

        conn.commit()

        payroll_id = cursor.lastrowid

        conn.close()

        return payroll_id

    # ==========================================
    # Update Payroll
    # ==========================================

    @staticmethod
    def update(payroll_id, data):

        net_salary = (
            float(data["basic_salary"])
            + float(data["allowances"])
            - float(data["deductions"])
        )

        conn = PayrollService.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        UPDATE payroll

        SET

            basic_salary=?,
            allowances=?,
            deductions=?,
            net_salary=?,
            pay_month=?,
            payment_date=?,
            status=?

        WHERE payroll_id=?

        """, (

            data["basic_salary"],
            data["allowances"],
            data["deductions"],
            net_salary,
            data["pay_month"],
            data["payment_date"],
            data["status"],
            payroll_id

        ))

        conn.commit()

        conn.close()

        return True

    # ==========================================
    # Delete Payroll
    # ==========================================

    @staticmethod
    def delete(payroll_id):

        conn = PayrollService.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        DELETE FROM payroll

        WHERE payroll_id=?

        """, (payroll_id,))

        conn.commit()

        conn.close()

        return True

    # ==========================================
    # Payroll Summary
    # ==========================================

    @staticmethod
    def payroll_summary():

        conn = PayrollService.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        SELECT

            COUNT(*) total_employees,

            SUM(net_salary) total_salary,

            AVG(net_salary) average_salary

        FROM payroll

        """)

        summary = dict(cursor.fetchone())

        conn.close()

        return summary