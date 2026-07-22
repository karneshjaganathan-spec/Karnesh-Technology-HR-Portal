from flask import Blueprint, jsonify, request

from middleware.auth_middleware import login_required, hr_required
from services.permission_service import PermissionService

permission_bp = Blueprint(
    "permission",
    __name__,
    url_prefix="/api/permissions"
)


# ==========================================
# Get All Permissions
# ==========================================

@permission_bp.route("/", methods=["GET"])
@login_required
def get_permissions():

    permissions = PermissionService.get_permissions()

    return jsonify({

        "success": True,
        "count": len(permissions),
        "data": permissions

    })


# ==========================================
# Get Permissions For Role
# ==========================================

@permission_bp.route("/role/<int:role_id>", methods=["GET"])
@login_required
def get_role_permissions(role_id):

    permissions = PermissionService.get_role_permissions(role_id)

    return jsonify({

        "success": True,
        "role_id": role_id,
        "permissions": permissions

    })


# ==========================================
# Update Role Permissions
# ==========================================

@permission_bp.route("/role/<int:role_id>", methods=["PUT"])
@hr_required
def update_role_permissions(role_id):

    data = request.get_json()

    permission_ids = data.get("permission_ids", [])

    PermissionService.update_permissions(

        role_id,

        permission_ids

    )

    return jsonify({

        "success": True,
        "message": "Permissions updated successfully."

    })