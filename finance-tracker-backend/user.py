from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, unset_jwt_cookies
from werkzeug.security import generate_password_hash
import models
from extensions import db

user_bp = Blueprint("user", __name__, url_prefix="/user")

# Update user details, protected
@user_bp.route("/update", methods=["PUT"])
@jwt_required()
def update():
    data = request.get_json()
    user = models.User.query.get(get_jwt_identity())

    # Validations
    if not user:
        return jsonify({"message": "User not found, please log in again"}), 404

    if "username" in data:
        user.username = data["username"]
    if "password" in data:
        user.password_hash = generate_password_hash(data["password"])
    if "email" in data:
        user.email = data["email"]

    db.session.commit()

    response = jsonify({"message": "User updated successfully"})
    unset_jwt_cookies(response)
    return response


# Delete user profile, protected
@user_bp.route("/delete", methods=["DELETE"])
@jwt_required()
def delete():
    user = models.User.query.get(get_jwt_identity())

    if not user:
        return jsonify({"message": "User not founds, please log in again"}), 404

    db.session.delete(user)
    db.session.commit()

    response = jsonify({"message": "User deleted successfully"})
    unset_jwt_cookies(response)
    return response

