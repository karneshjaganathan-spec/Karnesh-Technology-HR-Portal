from flask import Blueprint, request, jsonify

from middleware.auth_middleware import login_required, hr_required
from services.settings_service import SettingsService

settings_bp = Blueprint(
    "settings",
    __name__,
    url_prefix="/api/settings"
)


# ==========================================
# Get Settings
# ==========================================

@settings_bp.route("/", methods=["GET"])
@login_required
def get_settings():

    settings = SettingsService.get()

    return jsonify({

        "success": True,

        "data": settings

    })


# ==========================================
# Update Settings
# ==========================================

@settings_bp.route("/", methods=["PUT"])
@hr_required
def update_settings():

    data = request.get_json()

    required = [

        "company_name",

        "company_email",

        "company_phone",

        "company_address",

        "company_website",

        "working_hours_start",

        "working_hours_end",

        "leave_per_year",

        "currency",

        "timezone"

    ]

    for field in required:

        if field not in data:

            return jsonify({

                "success": False,

                "message": f"{field} is required."

            }), 400

    SettingsService.update(data)

    return jsonify({

        "success": True,

        "message": "Settings updated successfully."

    })