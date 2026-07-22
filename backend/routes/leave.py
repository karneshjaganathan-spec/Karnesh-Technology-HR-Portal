from flask import Blueprint, request, jsonify

from services.leave_service import LeaveService
from middleware.auth_middleware import login_required, hr_required

leave_bp = Blueprint(
    "leave",
    __name__,
    url_prefix="/api/leaves"
)


# ==========================================
# Get All Leave Requests
# ==========================================

@leave_bp.route("/", methods=["GET"])
@login_required
def get_leaves():

    leaves = LeaveService.get_all()

    return jsonify({
        "success": True,
        "count": len(leaves),
        "data": leaves
    })


# ==========================================
# Get Leave By ID
# ==========================================

@leave_bp.route("/<int:leave_id>", methods=["GET"])
@login_required
def get_leave(leave_id):

    leave = LeaveService.get_by_id(leave_id)

    if leave is None:

        return jsonify({
            "success": False,
            "message": "Leave request not found."
        }), 404

    return jsonify({
        "success": True,
        "data": leave
    })


# ==========================================
# Apply Leave
# ==========================================

@leave_bp.route("/", methods=["POST"])
@login_required
def apply_leave():
    print("POST /api/leaves called")
    
    data = request.get_json()

    required = [
        "employee_id",
        "leave_type",
        "start_date",
        "end_date",
        "reason",
        "status",
        "applied_on"
    ]

    for field in required:

        if field not in data:

            return jsonify({
                "success": False,
                "message": f"{field} is required."
            }), 400

    leave_id = LeaveService.add(data)

    return jsonify({
        "success": True,
        "leave_id": leave_id,
        "message": "Leave request submitted successfully."
    }), 201


# ==========================================
# Update Leave
# ==========================================

@leave_bp.route("/<int:leave_id>", methods=["PUT"])
@login_required
def update_leave(leave_id):

    leave = LeaveService.get_by_id(leave_id)

    if leave is None:

        return jsonify({
            "success": False,
            "message": "Leave request not found."
        }), 404

    data = request.get_json()

    LeaveService.update(leave_id, data)

    return jsonify({
        "success": True,
        "message": "Leave updated successfully."
    })


# ==========================================
# Delete Leave
# ==========================================

@leave_bp.route("/<int:leave_id>", methods=["DELETE"])
@hr_required
def delete_leave(leave_id):

    leave = LeaveService.get_by_id(leave_id)

    if leave is None:

        return jsonify({
            "success": False,
            "message": "Leave request not found."
        }), 404

    LeaveService.delete(leave_id)

    return jsonify({
        "success": True,
        "message": "Leave deleted successfully."
    })


# ==========================================
# Approve / Reject Leave
# ==========================================

@leave_bp.route("/<int:leave_id>/status", methods=["PUT"])
@hr_required
def update_leave_status(leave_id):

    data = request.get_json()

    status = data.get("status")

    if status not in ["Pending", "Approved", "Rejected"]:

        return jsonify({
            "success": False,
            "message": "Invalid leave status."
        }), 400

    LeaveService.change_status(leave_id, status)

    return jsonify({
        "success": True,
        "message": f"Leave {status.lower()} successfully."
    })


# ==========================================
# Employee Leave History
# ==========================================

@leave_bp.route("/employee/<int:employee_id>", methods=["GET"])
@login_required
def employee_history(employee_id):

    history = LeaveService.employee_history(employee_id)

    return jsonify({
        "success": True,
        "count": len(history),
        "data": history
    })


# ==========================================
# Search Leave
# ==========================================

@leave_bp.route("/search", methods=["GET"])
@login_required
def search_leave():

    status = request.args.get("status", "")

    leaves = LeaveService.search(status)

    return jsonify({
        "success": True,
        "count": len(leaves),
        "data": leaves
    })


# ==========================================
# Pending Leave Count
# ==========================================

@leave_bp.route("/pending-count", methods=["GET"])
@login_required
def pending_count():

    return jsonify({
        "success": True,
        "pending_leaves": LeaveService.pending_count()
    })