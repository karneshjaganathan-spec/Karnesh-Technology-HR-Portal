from flask import Blueprint, jsonify, request

from services.department_service import DepartmentService
from middleware.auth_middleware import login_required, hr_required

department_bp = Blueprint(
    "department",
    __name__,
    url_prefix="/api/departments"
)


# =====================================
# Get All Departments
# =====================================
@department_bp.route("/", methods=["GET"])
@login_required
def get_departments():

    departments = DepartmentService.get_all()

    return jsonify({
        "success": True,
        "count": len(departments),
        "data": departments
    })


# =====================================
# Get Department By ID
# =====================================
@department_bp.route("/<int:department_id>", methods=["GET"])
@login_required
def get_department(department_id):

    department = DepartmentService.get_by_id(department_id)

    if department is None:

        return jsonify({
            "success": False,
            "message": "Department not found."
        }), 404

    return jsonify({
        "success": True,
        "data": department
    })


# =====================================
# Add Department
# =====================================
@department_bp.route("/", methods=["POST"])
@hr_required
def add_department():

    data = request.get_json()

    department_id = DepartmentService.add(data)

    return jsonify({
        "success": True,
        "department_id": department_id,
        "message": "Department added successfully."
    })


# =====================================
# Update Department
# =====================================
@department_bp.route("/<int:department_id>", methods=["PUT"])
@hr_required
def update_department(department_id):

    data = request.get_json()

    DepartmentService.update(department_id, data)

    return jsonify({
        "success": True,
        "message": "Department updated successfully."
    })


# =====================================
# Delete Department
# =====================================
@department_bp.route("/<int:department_id>", methods=["DELETE"])
@hr_required
def delete_department(department_id):

    DepartmentService.delete(department_id)

    return jsonify({
        "success": True,
        "message": "Department deleted successfully."
    })