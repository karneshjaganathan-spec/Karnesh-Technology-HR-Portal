from flask import Blueprint, jsonify, request, session

from middleware.auth_middleware import login_required
from services.profile_service import ProfileService

profile_bp = Blueprint(
    "profile",
    __name__,
    url_prefix="/api/profile"
)


# ==========================================
# Get Logged In User Profile
# ==========================================

@profile_bp.route("/", methods=["GET"])
@login_required
def get_profile():

    user_id = session.get("user_id")

    profile = ProfileService.get_profile(user_id)

    if profile is None:

        return jsonify({
            "success": False,
            "message": "Profile not found."
        }), 404

    return jsonify({
        "success": True,
        "data": profile
    })


# ==========================================
# Update Profile
# ==========================================

@profile_bp.route("/", methods=["PUT"])
@login_required
def update_profile():

    user_id = session.get("user_id")

    data = request.get_json()

    required = [
        "email",
        "phone",
        "address"
    ]

    for field in required:

        if field not in data:

            return jsonify({
                "success": False,
                "message": f"{field} is required."
            }), 400

    ProfileService.update_profile(user_id, data)

    return jsonify({
        "success": True,
        "message": "Profile updated successfully."
    })


# ==========================================
# Change Password
# ==========================================

@profile_bp.route("/change-password", methods=["PUT"])
@login_required
def change_password():

    user_id = session.get("user_id")

    data = request.get_json()

    current_password = data.get("current_password", "").strip()

    new_password = data.get("new_password", "").strip()

    confirm_password = data.get("confirm_password", "").strip()

    if not current_password or not new_password:

        return jsonify({
            "success": False,
            "message": "Password fields cannot be empty."
        }), 400

    if new_password != confirm_password:

        return jsonify({
            "success": False,
            "message": "Passwords do not match."
        }), 400

    profile = ProfileService.get_profile(user_id)

    if profile is None:

        return jsonify({
            "success": False,
            "message": "User not found."
        }), 404

    # NOTE:
    # Replace this with password hashing verification
    # if you implement bcrypt later.

    ProfileService.change_password(user_id, new_password)

    return jsonify({
        "success": True,
        "message": "Password changed successfully."
    })