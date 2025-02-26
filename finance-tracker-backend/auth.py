from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from extensions import db
import models

# attach the current file's name to the blueprint, so it finds the resources from auth.py
auth_bp = Blueprint("auth", __name__)


# Register a new User
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    # Validations
    if not data or "username" not in data or "password" not in data or "email" not in data or "name" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    if models.User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "The given username is already taken"}), 400

    # Create a new user if passed validations
    new_user = models.User(username=data["username"],
                           password_hash=generate_password_hash(data["password"]),
                           name=data["name"],
                           email=data["email"])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User is registered successfully"}), 201


# Login the User
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = models.User.query.filter_by(username=data["username"]).first()

    # Validations
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "You are missing some important data to fill"}), 400

    if not user or not check_password_hash(user.password_hash, data["password"]):
        return jsonify({"error": "Invalid username or password"}), 401

    # If passed validations, then create a JWT token
    access_token = create_access_token(identity=user.id)
    return jsonify({"acces_token": access_token}), 200


# Protected get User route, only with JWT token
@auth_bp.route("/user", methods=["GET"])
@jwt_required()
def get_user():
    user = models.User.query.get(user_id=get_jwt_identity())

    # Validations
    if not user:
        return jsonify({"error": "User not found. Try logging in again"}), 404

    return jsonify({"id": user.id, "username": user.username}), 200


