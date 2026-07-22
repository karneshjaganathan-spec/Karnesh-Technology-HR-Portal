from flask import Blueprint, request, jsonify, session
from services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "No data received"
        }), 400

    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    if username == "" or password == "":
        return jsonify({
            "success": False,
            "message": "Username and Password are required"
        }), 400

    user = AuthService.login(username, password)

    if not user:
        return jsonify({
            "success": False,
            "message": "Invalid username or password"
        }), 401

    session["user_id"] = user["id"]
    session["username"] = user["username"]
    session["role_id"] = user["role_id"]

    return jsonify({
        "success": True,
        "message": "Login Successful",
        "user": user
    })


@auth_bp.route("/logout", methods=["POST"])
def logout():

    session.clear()

    return jsonify({
        "success": True,
        "message": "Logged out successfully"
    })


@auth_bp.route("/me", methods=["GET"])
def current_user():

    if "user_id" not in session:
        return jsonify({
            "logged_in": False
        })

    return jsonify({
        "logged_in": True,
        "user": {
            "id": session.get("user_id"),
            "username": session.get("username"),
            "role_id": session.get("role_id")
        }
    })