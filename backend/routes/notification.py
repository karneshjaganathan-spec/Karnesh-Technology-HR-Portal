from flask import Blueprint, jsonify, request

from middleware.auth_middleware import login_required, hr_required
from services.notification_service import NotificationService

notification_bp = Blueprint(
    "notification",
    __name__,
    url_prefix="/api/notifications"
)


# ==========================================
# Get All Notifications
# ==========================================

@notification_bp.route("/", methods=["GET"])
@login_required
def get_notifications():

    notifications = NotificationService.get_all()

    return jsonify({

        "success": True,
        "count": len(notifications),
        "data": notifications

    })


# ==========================================
# Get Notification By ID
# ==========================================

@notification_bp.route("/<int:notification_id>", methods=["GET"])
@login_required
def get_notification(notification_id):

    notification = NotificationService.get(notification_id)

    if notification is None:

        return jsonify({

            "success": False,
            "message": "Notification not found."

        }), 404

    return jsonify({

        "success": True,
        "data": notification

    })


# ==========================================
# Create Notification
# ==========================================

@notification_bp.route("/", methods=["POST"])
@hr_required
def add_notification():

    data = request.get_json()

    required = [

        "title",
        "message",
        "notification_type",
        "recipient_type"

    ]

    for field in required:

        if field not in data:

            return jsonify({

                "success": False,
                "message": f"{field} is required."

            }), 400

    notification_id = NotificationService.add(data)

    return jsonify({

        "success": True,
        "notification_id": notification_id,
        "message": "Notification created successfully."

    }), 201


# ==========================================
# Mark Notification As Read
# ==========================================

@notification_bp.route("/<int:notification_id>/read", methods=["PUT"])
@login_required
def mark_read(notification_id):

    notification = NotificationService.get(notification_id)

    if notification is None:

        return jsonify({

            "success": False,
            "message": "Notification not found."

        }), 404

    NotificationService.mark_read(notification_id)

    return jsonify({

        "success": True,
        "message": "Notification marked as read."

    })


# ==========================================
# Delete Notification
# ==========================================

@notification_bp.route("/<int:notification_id>", methods=["DELETE"])
@hr_required
def delete_notification(notification_id):

    notification = NotificationService.get(notification_id)

    if notification is None:

        return jsonify({

            "success": False,
            "message": "Notification not found."

        }), 404

    NotificationService.delete(notification_id)

    return jsonify({

        "success": True,
        "message": "Notification deleted successfully."

    })