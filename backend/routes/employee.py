from flask import Blueprint, request, jsonify

from services.employee_service import EmployeeService
from middleware.auth_middleware import login_required, hr_required

employee_bp = Blueprint(
    "employee",
    __name__,
    url_prefix="/api/employees"
)


# =====================================================
# Get All Employees
# =====================================================
@employee_bp.route("/", methods=["GET"])
@login_required
def get_all_employees():

    employees = EmployeeService.get_all()

    return jsonify({
        "success": True,
        "count": len(employees),
        "data": employees
    })


# =====================================================
# Get Employee By ID
# =====================================================
@employee_bp.route("/<int:employee_id>", methods=["GET"])
@login_required
def get_employee(employee_id):

    employee = EmployeeService.get_by_id(employee_id)

    if employee is None:
        return jsonify({
            "success": False,
            "message": "Employee not found."
        }), 404

    return jsonify({
        "success": True,
        "data": employee
    })


# =====================================================
# Add Employee
# =====================================================
@employee_bp.route("/", methods=["POST"])
@hr_required
def add_employee():

    try:

        data = request.get_json()

        existing = EmployeeService.employee_exists(
            data["employee_code"],
            data["user_id"]
        )

        if existing:

            if existing["employee_code"] == data["employee_code"]:
                return jsonify({
                    "success": False,
                    "message": "Employee Code is already assigned."
                }), 409

            if existing["user_id"] == data["user_id"]:
                return jsonify({
                    "success": False,
                    "message": "User ID is already assigned."
                }), 409

        required_fields = [
            "employee_code",
            "first_name",
            "last_name",
            "gender",
            "dob",
            "email",
            "phone",
            "address",
            "designation",
            "salary",
            "joining_date",
            "department_id",
            "user_id",
            "status"
        ]

        for field in required_fields:
            if field not in data:
                return jsonify({
                    "success": False,
                    "message": f"{field} is required."
                }), 400

        employee_id = EmployeeService.add(data)

        return jsonify({
            "success": True,
            "message": "Employee added successfully.",
            "employee_id": employee_id
        }), 201

    except Exception as e:

        import traceback
        traceback.print_exc()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
# =====================================================
# Update Employee
# =====================================================
@employee_bp.route("/<int:employee_id>", methods=["PUT"])
@hr_required
def update_employee(employee_id):

    employee = EmployeeService.get_by_id(employee_id)

    if employee is None:
        return jsonify({
            "success": False,
            "message": "Employee not found."
        }), 404

    data = request.get_json()

    EmployeeService.update(employee_id, data)

    return jsonify({
        "success": True,
        "message": "Employee updated successfully."
    })


# =====================================================
# Delete Employee
# =====================================================
@employee_bp.route("/<int:employee_id>", methods=["DELETE"])
@hr_required
def delete_employee(employee_id):

    employee = EmployeeService.get_by_id(employee_id)

    if employee is None:
        return jsonify({
            "success": False,
            "message": "Employee not found."
        }), 404

    EmployeeService.delete(employee_id)

    return jsonify({
        "success": True,
        "message": "Employee deleted successfully."
    })


# =====================================================
# Search Employee
# =====================================================
@employee_bp.route("/search", methods=["GET"])
@login_required
def search_employee():

    keyword = request.args.get("q", "").strip()

    employees = EmployeeService.search(keyword)

    return jsonify({
        "success": True,
        "count": len(employees),
        "data": employees
    })


# =====================================================
# Employee Statistics
# =====================================================
@employee_bp.route("/stats", methods=["GET"])
@login_required
def employee_statistics():

    return jsonify({
        "success": True,
        "total_employees": EmployeeService.count(),
        "active_employees": EmployeeService.active_count()
    })