from flask import Flask, request, jsonify
from pymongo import MongoClient
import random

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["stiffy"]  
users_collection = db["members"]  

def generate_account_id():
    return random.randint(1000, 9999)  

@app.route("/register/manager", methods=["POST"])
def register_manager():
    data = request.get_json()
    if "name" not in data or "email" not in data or "passcode" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    account_id = generate_account_id()

    manager = {
        "name": data["name"],
        "email": data["email"],
        "role": "manager",
        "account_id": account_id,
        "passcode": data["passcode"]
    }
    users_collection.insert_one(manager)

    return jsonify({"message": "Manager account created successfully", "account_id": account_id}), 201

@app.route("/register/salesperson", methods=["POST"])
def register_salesperson():

    data = request.get_json()
    if "name" not in data or "email" not in data or "passcode" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    manager = users_collection.find_one({"passcode": data["passcode"], "role": "manager"})
    if not manager:
        return jsonify({"error": "Invalid passcode"}), 400

    salesperson = {
        "name": data["name"],
        "email": data["email"],
        "role": "salesperson",
        "account_id": manager["account_id"]
    }
    users_collection.insert_one(salesperson)

    return jsonify({"message": "Salesperson account created successfully", "account_id": manager["account_id"]}), 201


@app.route("/users/<int:account_id>", methods=["GET"])
def get_users_by_account_id(account_id):
    users = list(users_collection.find({"account_id": account_id}, {"_id": 0, "passcode": 0}))
    if not users:
        return jsonify({"error": "No users found for this account_id"}), 404

    return jsonify(users)

if __name__ == "__main__":
    app.run(debug=True)
