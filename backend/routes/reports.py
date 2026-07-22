from flask import Blueprint, jsonify

from middleware.auth_middleware import login_required, hr_required
from services.report_service import ReportService

reports_bp = Blueprint(
    "reports",
    __name__,
    url_prefix="/api/reports"
)


# ==========================================
# Dashboard Summary Report
# ==========================================

@reports_bp.route("/dashboard", methods=["GET"])
@login_required
def dashboard_report():

    report = ReportService.dashboard_summary()

    return jsonify({
        "success": True,
        "data": report
    })


# ==========================================
# Department Report
# ==========================================

@reports_bp.route("/departments", methods=["GET"])
@login_required
def department_report():

    report = ReportService.department_report()

    return jsonify({
        "success": True,
        "count": len(report),
        "data": report
    })


# ==========================================
# Attendance Report
# ==========================================

@reports_bp.route("/attendance", methods=["GET"])
@login_required
def attendance_report():

    report = ReportService.attendance_report()

    return jsonify({
        "success": True,
        "count": len(report),
        "data": report
    })


# ==========================================
# Leave Report
# ==========================================

@reports_bp.route("/leaves", methods=["GET"])
@login_required
def leave_report():

    report = ReportService.leave_report()

    return jsonify({
        "success": True,
        "count": len(report),
        "data": report
    })


# ==========================================
# Salary Report
# ==========================================

@reports_bp.route("/salary", methods=["GET"])
@hr_required
def salary_report():

    report = ReportService.salary_report()

    return jsonify({
        "success": True,
        "count": len(report),
        "data": report
    })