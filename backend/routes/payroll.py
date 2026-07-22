from flask import Blueprint, request, jsonify

from middleware.auth_middleware import login_required, hr_required
from services.payroll_service import PayrollService

payroll_bp = Blueprint(
    "payroll",
    __name__,
    url_prefix="/api/payroll"
)


# ==========================================
# Get All Payroll
# ==========================================

@payroll_bp.route("/", methods=["GET"])
@login_required
def get_payroll():

    payroll = PayrollService.get_all()

    return jsonify({
        "success": True,
        "count": len(payroll),
        "data": payroll
    })


# ==========================================
# Get Payroll By ID
# ==========================================

@payroll_bp.route("/<int:payroll_id>", methods=["GET"])
@login_required
def get_payroll_by_id(payroll_id):

    payroll = PayrollService.get_by_id(payroll_id)

    if payroll is None:

        return jsonify({
            "success": False,
            "message": "Payroll record not found."
        }), 404

    return jsonify({
        "success": True,
        "data": payroll
    })


# ==========================================
# Generate Payroll
# ==========================================

@payroll_bp.route("/", methods=["POST"])
@hr_required
def generate_payroll():

    data = request.get_json()

    required = [

        "employee_id",
        "basic_salary",
        "allowances",
        "deductions",
        "pay_month",
        "payment_date",
        "status"

    ]

    for field in required:

        if field not in data:

            return jsonify({

                "success": False,
                "message": f"{field} is required."

            }), 400

    payroll_id = PayrollService.add(data)

    return jsonify({

        "success": True,
        "payroll_id": payroll_id,
        "message": "Payroll generated successfully."

    }), 201


# ==========================================
# Update Payroll
# ==========================================

@payroll_bp.route("/<int:payroll_id>", methods=["PUT"])
@hr_required
def update_payroll(payroll_id):

    payroll = PayrollService.get_by_id(payroll_id)

    if payroll is None:

        return jsonify({

            "success": False,
            "message": "Payroll record not found."

        }), 404

    PayrollService.update(

        payroll_id,

        request.get_json()

    )

    return jsonify({

        "success": True,
        "message": "Payroll updated successfully."

    })


# ==========================================
# Delete Payroll
# ==========================================

@payroll_bp.route("/<int:payroll_id>", methods=["DELETE"])
@hr_required
def delete_payroll(payroll_id):

    payroll = PayrollService.get_by_id(payroll_id)

    if payroll is None:

        return jsonify({

            "success": False,
            "message": "Payroll record not found."

        }), 404

    PayrollService.delete(payroll_id)

    return jsonify({

        "success": True,
        "message": "Payroll deleted successfully."

    })


# ==========================================
# Payroll Summary
# ==========================================

@payroll_bp.route("/summary", methods=["GET"])
@login_required
def payroll_summary():

    summary = PayrollService.payroll_summary()

    return jsonify({

        "success": True,
        "data": summary

    })