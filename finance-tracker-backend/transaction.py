from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
import models

transaction_bp = Blueprint("transaction", __name__, url_prefix="/transaction")


# Create a new transaction
@transaction_bp.route("/create", methods=["POST"])
@jwt_required()
def create_transaction():
    data = request.get_json()
    user_id = get_jwt_identity()

    # Validations
    if not data or "category" not in data or "amount" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    new_transaction = models.Transaction(
        user_id=user_id,
        amount=data["amount"],
        category=data["category"],
        date=data["date"],
        description=data["description"]
    )

    db.session.add(new_transaction)
    db.session.commit()
    return jsonify({"message": "New transaction added successfully!"}), 201


# Retrieval of transactions for a give User
@transaction_bp.route("/all", methods=["GET"])
@jwt_required()
def get_transactions():
    user_id = get_jwt_identity()
    transactions = models.Transaction.query.filter_by(user_id=user_id).all()

    # Validations
    if not transactions:
        return jsonify({"message": "No transaction found for this user"}), 404

    return jsonify([{"id": transaction.id, "amount": transaction.amount, "cetegory": transaction.category, "date": transaction.date, "description": transaction.description} for transaction in transactions])


# Get a specific transaction based on ID
@transaction_bp.route("/<int:transaction_id>", methods=["GET"])
@jwt_required()
def get_transaction(transaction_id):
    user_id = get_jwt_identity()
    transaction = models.Transaction.query.filter_by(id=transaction_id, user_id=user_id)

    # Validations
    if not transaction:
        return jsonify({"message": "Transaction not founds"}), 404

    return jsonify({"id": transaction.id, "amount": transaction.amount, "category": transaction.category, "date": transaction.date, "description": transaction.description})


# Update a specific transaction
@transaction_bp.route("/update/<int_transaction_id>", methods=["PUT"])
@jwt_required()
def update_transaction(transaction_id):
    user_id = get_jwt_identity()
    transaction = models.Transaction.query.filter_by(id=transaction_id).first()
    data = request.get_json()

    # Validations
    if not transaction:
        return jsonify({"message": "Transaction not founds"}), 404

    if "amount" in data:
        transaction.amount = data["amount"]
    if "category" in data:
        transaction.category = data["category"]
    if "description" in data:
        transaction.description = data["description"]
    if "date" in data:
        transaction.date = data["date"]

    db.session.commit()
    return jsonify({"message": "Transaction updated successfully"})


# Delete a given transaction
@transaction_bp.route("/delete/<int:transaction_id>", methods=["DELETE"])
@jwt_required()
def delete_transaction(transaction_id):
    user_id = get_jwt_identity()
    transaction = models.Transaction.query.filter_by(id=transaction_id)

    # Validations
    if not transaction:
        return jsonify({"message": "Transaction not founds"}), 404

    db.session.delete(transaction)
    db.session.commit()
    return jsonify({"message": "Transaction deleted successfully"})

