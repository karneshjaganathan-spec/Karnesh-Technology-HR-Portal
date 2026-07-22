from flask import Blueprint, request, jsonify

from middleware.auth_middleware import login_required, hr_required
from services.recruitment_service import RecruitmentService

recruitment_bp = Blueprint(
    "recruitment",
    __name__,
    url_prefix="/api/recruitment"
)


# ==========================================
# Get All Jobs
# ==========================================

@recruitment_bp.route("/jobs", methods=["GET"])
@login_required
def get_jobs():

    jobs = RecruitmentService.get_jobs()

    return jsonify({
        "success": True,
        "count": len(jobs),
        "data": jobs
    })


# ==========================================
# Get Job By ID
# ==========================================

@recruitment_bp.route("/jobs/<int:job_id>", methods=["GET"])
@login_required
def get_job(job_id):

    job = RecruitmentService.get_job(job_id)

    if job is None:

        return jsonify({
            "success": False,
            "message": "Job not found."
        }), 404

    return jsonify({
        "success": True,
        "data": job
    })


# ==========================================
# Add Job
# ==========================================

@recruitment_bp.route("/jobs", methods=["POST"])
@hr_required
def add_job():

    data = request.get_json()

    required = [

        "job_title",
        "department",
        "vacancies",
        "experience",
        "location",
        "description",
        "status"

    ]

    for field in required:

        if field not in data:

            return jsonify({
                "success": False,
                "message": f"{field} is required."
            }), 400

    job_id = RecruitmentService.add_job(data)

    return jsonify({

        "success": True,
        "job_id": job_id,
        "message": "Job created successfully."

    }), 201


# ==========================================
# Update Job
# ==========================================

@recruitment_bp.route("/jobs/<int:job_id>", methods=["PUT"])
@hr_required
def update_job(job_id):

    if RecruitmentService.get_job(job_id) is None:

        return jsonify({

            "success": False,
            "message": "Job not found."

        }), 404

    RecruitmentService.update_job(

        job_id,

        request.get_json()

    )

    return jsonify({

        "success": True,
        "message": "Job updated successfully."

    })


# ==========================================
# Delete Job
# ==========================================

@recruitment_bp.route("/jobs/<int:job_id>", methods=["DELETE"])
@hr_required
def delete_job(job_id):

    if RecruitmentService.get_job(job_id) is None:

        return jsonify({

            "success": False,
            "message": "Job not found."

        }), 404

    RecruitmentService.delete_job(job_id)

    return jsonify({

        "success": True,
        "message": "Job deleted successfully."

    })


# ==========================================
# Candidate List
# ==========================================

@recruitment_bp.route("/candidates", methods=["GET"])
@login_required
def candidates():

    data = RecruitmentService.get_candidates()

    return jsonify({

        "success": True,
        "count": len(data),
        "data": data

    })


# ==========================================
# Candidate Status
# ==========================================

@recruitment_bp.route(
    "/candidates/<int:candidate_id>/status",
    methods=["PUT"]
)
@hr_required
def update_status(candidate_id):

    data = request.get_json()

    RecruitmentService.update_candidate_status(

        candidate_id,

        data["status"]

    )

    return jsonify({

        "success": True,
        "message": "Candidate status updated."

    })