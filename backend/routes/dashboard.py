from flask import Blueprint, jsonify

from middleware.auth_middleware import login_required
from services.dashboard_service import DashboardService

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/api/dashboard"
)


# ==========================================================
# Dashboard Statistics
# ==========================================================
@dashboard_bp.route("/stats", methods=["GET"])
@login_required
def dashboard_stats():

    stats = DashboardService.get_dashboard_stats()

    return jsonify({
        "success": True,
        "data": stats
    })


# ==========================================================
# Recent Employees
# ==========================================================
@dashboard_bp.route("/recent-employees", methods=["GET"])
@login_required
def recent_employees():

    employees = DashboardService.recent_employees()

    return jsonify({
        "success": True,
        "count": len(employees),
        "data": employees
    })


# ==========================================================
# Department Summary
# ==========================================================
@dashboard_bp.route("/departments", methods=["GET"])
@login_required
def department_summary():

    summary = DashboardService.department_summary()

    return jsonify({
        "success": True,
        "count": len(summary),
        "data": summary
    })