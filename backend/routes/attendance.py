from flask import Blueprint, request, jsonify

from services.attendance_service import AttendanceService
from middleware.auth_middleware import login_required, hr_required

attendance_bp = Blueprint(
    "attendance",
    __name__,
    url_prefix="/api/attendance"
)


# ==========================================
# Get All Attendance
# ==========================================

@attendance_bp.route("/", methods=["GET"])
@login_required
def get_attendance():

    attendance = AttendanceService.get_all()

    return jsonify({
        "success": True,
        "count": len(attendance),
        "data": attendance
    })


# ==========================================
# Get Attendance By ID
# ==========================================

@attendance_bp.route("/<int:attendance_id>", methods=["GET"])
@login_required
def get_attendance_by_id(attendance_id):

    attendance = AttendanceService.get_by_id(attendance_id)

    if attendance is None:

        return jsonify({
            "success": False,
            "message": "Attendance record not found."
        }), 404

    return jsonify({
        "success": True,
        "data": attendance
    })


# ==========================================
# Mark Attendance
# ==========================================

@attendance_bp.route("/", methods=["POST"])
@hr_required
def mark_attendance():

    data = request.get_json()

    required = [
        "employee_id",
        "attendance_date",
        "check_in",
        "check_out",
        "status"
    ]

    for field in required:

        if field not in data:

            return jsonify({
                "success": False,
                "message": f"{field} is required."
            }), 400

    attendance_id = AttendanceService.add(data)

    return jsonify({
        "success": True,
        "attendance_id": attendance_id,
        "message": "Attendance marked successfully."
    }), 201


# ==========================================
# Update Attendance
# ==========================================

@attendance_bp.route("/<int:attendance_id>", methods=["PUT"])
@hr_required
def update_attendance(attendance_id):

    attendance = AttendanceService.get_by_id(attendance_id)

    if attendance is None:

        return jsonify({
            "success": False,
            "message": "Attendance record not found."
        }), 404

    data = request.get_json()

    AttendanceService.update(attendance_id, data)

    return jsonify({
        "success": True,
        "message": "Attendance updated successfully."
    })


# ==========================================
# Delete Attendance
# ==========================================

@attendance_bp.route("/<int:attendance_id>", methods=["DELETE"])
@hr_required
def delete_attendance(attendance_id):

    attendance = AttendanceService.get_by_id(attendance_id)

    if attendance is None:

        return jsonify({
            "success": False,
            "message": "Attendance record not found."
        }), 404

    AttendanceService.delete(attendance_id)

    return jsonify({
        "success": True,
        "message": "Attendance deleted successfully."
    })


# ==========================================
# Search Attendance by Date
# ==========================================

@attendance_bp.route("/search", methods=["GET"])
@login_required
def search_attendance():

    date = request.args.get("date", "")

    attendance = AttendanceService.search(date)

    return jsonify({
        "success": True,
        "count": len(attendance),
        "data": attendance
    })


# ==========================================
# Employee Attendance History
# ==========================================

@attendance_bp.route("/employee/<int:employee_id>", methods=["GET"])
@login_required
def employee_history(employee_id):

    history = AttendanceService.employee_history(employee_id)

    return jsonify({
        "success": True,
        "count": len(history),
        "data": history
    })


# ==========================================
# Today's Attendance Count
# ==========================================

@attendance_bp.route("/today-count", methods=["GET"])
@login_required
def today_count():

    return jsonify({
        "success": True,
        "today_attendance": AttendanceService.today_count()
    })