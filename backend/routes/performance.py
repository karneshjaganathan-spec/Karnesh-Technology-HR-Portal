from flask import Blueprint, jsonify, request

from middleware.auth_middleware import login_required, hr_required
from services.performance_service import PerformanceService

performance_bp = Blueprint(
    "performance",
    __name__,
    url_prefix="/api/performance"
)


# ==========================================
# Get All Performance Reviews
# ==========================================

@performance_bp.route("/", methods=["GET"])
@login_required
def get_reviews():

    reviews = PerformanceService.get_all()

    return jsonify({

        "success": True,
        "count": len(reviews),
        "data": reviews

    })


# ==========================================
# Get Single Review
# ==========================================

@performance_bp.route("/<int:review_id>", methods=["GET"])
@login_required
def get_review(review_id):

    review = PerformanceService.get(review_id)

    if review is None:

        return jsonify({

            "success": False,
            "message": "Performance review not found."

        }), 404

    return jsonify({

        "success": True,
        "data": review

    })


# ==========================================
# Add Review
# ==========================================

@performance_bp.route("/", methods=["POST"])
@hr_required
def add_review():

    data = request.get_json()

    required = [

        "employee_id",
        "review_period",
        "reviewer_name",
        "kpi_score",
        "attendance_score",
        "teamwork_score",
        "communication_score",
        "strengths",
        "improvements",
        "manager_comments",
        "employee_comments",
        "promotion_recommended",
        "review_date",
        "status"

    ]

    for field in required:

        if field not in data:

            return jsonify({

                "success": False,
                "message": f"{field} is required."

            }), 400

    review_id = PerformanceService.add(data)

    return jsonify({

        "success": True,
        "review_id": review_id,
        "message": "Performance review added successfully."

    }), 201


# ==========================================
# Delete Review
# ==========================================

@performance_bp.route("/<int:review_id>", methods=["DELETE"])
@hr_required
def delete_review(review_id):

    review = PerformanceService.get(review_id)

    if review is None:

        return jsonify({

            "success": False,
            "message": "Review not found."

        }), 404

    PerformanceService.delete(review_id)

    return jsonify({

        "success": True,
        "message": "Review deleted successfully."

    })