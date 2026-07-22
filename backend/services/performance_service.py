import sqlite3

DATABASE = "hr_portal.db"


class PerformanceService:

    @staticmethod
    def get_connection():

        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn


    # =====================================
    # All Reviews
    # =====================================

    @staticmethod
    def get_all():

        conn = PerformanceService.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        SELECT

            p.review_id,
            p.employee_id,

            e.employee_code,
            e.first_name,
            e.last_name,
            e.designation,

            p.review_period,
            p.overall_rating,
            p.reviewer_name,
            p.review_date,
            p.status

        FROM performance_reviews p

        INNER JOIN employees e

        ON p.employee_id=e.employee_id

        ORDER BY p.review_date DESC

        """)

        reviews = [

            dict(row)

            for row in cursor.fetchall()

        ]

        conn.close()

        return reviews


    # =====================================
    # Single Review
    # =====================================

    @staticmethod
    def get(review_id):

        conn = PerformanceService.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        SELECT *

        FROM performance_reviews

        WHERE review_id=?

        """, (review_id,))

        review = cursor.fetchone()

        conn.close()

        if review:

            return dict(review)

        return None


    # =====================================
    # Add Review
    # =====================================

    @staticmethod
    def add(data):

        overall = round(

            (

                float(data["kpi_score"])

                + float(data["attendance_score"])

                + float(data["teamwork_score"])

                + float(data["communication_score"])

            ) / 4,

            2

        )

        conn = PerformanceService.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        INSERT INTO performance_reviews(

            employee_id,

            review_period,

            reviewer_name,

            kpi_score,

            attendance_score,

            teamwork_score,

            communication_score,

            overall_rating,

            strengths,

            improvements,

            manager_comments,

            employee_comments,

            promotion_recommended,

            review_date,

            status

        )

        VALUES(

        ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?

        )

        """, (

            data["employee_id"],

            data["review_period"],

            data["reviewer_name"],

            data["kpi_score"],

            data["attendance_score"],

            data["teamwork_score"],

            data["communication_score"],

            overall,

            data["strengths"],

            data["improvements"],

            data["manager_comments"],

            data["employee_comments"],

            data["promotion_recommended"],

            data["review_date"],

            data["status"]

        ))

        conn.commit()

        review_id = cursor.lastrowid

        conn.close()

        return review_id


    # =====================================
    # Delete Review
    # =====================================

    @staticmethod
    def delete(review_id):

        conn = PerformanceService.get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        DELETE FROM performance_reviews

        WHERE review_id=?

        """, (review_id,))

        conn.commit()

        conn.close()

        return True