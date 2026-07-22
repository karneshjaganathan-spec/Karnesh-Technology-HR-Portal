from functools import wraps
from flask import session, jsonify


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:
            return jsonify({
                "success": False,
                "message": "Please login first."
            }), 401

        return func(*args, **kwargs)

    return wrapper


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:
            return jsonify({
                "success": False,
                "message": "Please login first."
            }), 401

        if session.get("role_id") != 1:
            return jsonify({
                "success": False,
                "message": "Administrator access required."
            }), 403

        return func(*args, **kwargs)

    return wrapper


def hr_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:
            return jsonify({
                "success": False,
                "message": "Please login first."
            }), 401

        if session.get("role_id") not in (1, 2):
            return jsonify({
                "success": False,
                "message": "HR/Admin access required."
            }), 403

        return func(*args, **kwargs)

    return wrapper