import sqlite3

DATABASE = "hr_portal.db"


class RecruitmentService:

    @staticmethod
    def get_connection():
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn

    # ==========================================
    # Get All Job Openings
    # ==========================================

    @staticmethod
    def get_jobs():

        conn = RecruitmentService.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM jobs
            ORDER BY created_at DESC
        """)

        jobs = [dict(row) for row in cursor.fetchall()]

        conn.close()

        return jobs

    # ==========================================
    # Get Job By ID
    # ==========================================

    @staticmethod
    def get_job(job_id):

        conn = RecruitmentService.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM jobs
            WHERE job_id=?
        """, (job_id,))

        job = cursor.fetchone()

        conn.close()

        if job:
            return dict(job)

        return None

    # ==========================================
    # Add Job
    # ==========================================

    @staticmethod
    def add_job(data):

        conn = RecruitmentService.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO jobs(
                job_title,
                department,
                vacancies,
                experience,
                location,
                description,
                status
            )
            VALUES(?,?,?,?,?,?,?)
        """, (

            data["job_title"],
            data["department"],
            data["vacancies"],
            data["experience"],
            data["location"],
            data["description"],
            data["status"]

        ))

        conn.commit()

        job_id = cursor.lastrowid

        conn.close()

        return job_id

    # ==========================================
    # Update Job
    # ==========================================

    @staticmethod
    def update_job(job_id, data):

        conn = RecruitmentService.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE jobs
            SET
                job_title=?,
                department=?,
                vacancies=?,
                experience=?,
                location=?,
                description=?,
                status=?
            WHERE job_id=?
        """, (

            data["job_title"],
            data["department"],
            data["vacancies"],
            data["experience"],
            data["location"],
            data["description"],
            data["status"],
            job_id

        ))

        conn.commit()

        conn.close()

        return True

    # ==========================================
    # Delete Job
    # ==========================================

    @staticmethod
    def delete_job(job_id):

        conn = RecruitmentService.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM jobs
            WHERE job_id=?
        """, (job_id,))

        conn.commit()

        conn.close()

        return True

    # ==========================================
    # Get Candidates
    # ==========================================

    @staticmethod
    def get_candidates():

        conn = RecruitmentService.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                c.*,
                j.job_title
            FROM candidates c
            LEFT JOIN jobs j
            ON c.job_id=j.job_id
            ORDER BY c.applied_date DESC
        """)

        candidates = [dict(row) for row in cursor.fetchall()]

        conn.close()

        return candidates

    # ==========================================
    # Update Candidate Status
    # ==========================================

    @staticmethod
    def update_candidate_status(candidate_id, status):

        conn = RecruitmentService.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE candidates
            SET status=?
            WHERE candidate_id=?
        """, (

            status,
            candidate_id

        ))

        conn.commit()

        conn.close()

        return True