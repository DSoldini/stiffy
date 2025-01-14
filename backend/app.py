from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["stiffy"]  
members_collection = db["members"]  

@app.route("/members", methods=["GET"])
def get_all_members():
   
    members = list(members_collection.find({}, {"_id": 0}))  
    return jsonify(members)

@app.route("/members", methods=["POST"])
def add_member():
    data = request.get_json()
    if "name" in data and "email" in data and "points" in data:
        members_collection.insert_one(data)
        return jsonify({"message": "Member added successfully!"}), 201
    return jsonify({"error": "Missing required fields"}), 400

@app.route("/members/<string:name>", methods=["GET"])
def get_member(name):
    member = members_collection.find_one({"name": name}, {"_id": 0})
    if member:
        return jsonify(member)
    return jsonify({"error": "Member not found"}), 404

@app.route("/members/<string:name>", methods=["PUT"])
def update_member(name):
    data = request.get_json()
    update_result = members_collection.update_one({"name": name}, {"$set": data})
    if update_result.matched_count > 0:
        return jsonify({"message": "Member updated successfully!"})
    return jsonify({"error": "Member not found"}), 404

@app.route("/members/<string:name>", methods=["DELETE"])
def delete_member(name):
    delete_result = members_collection.delete_one({"name": name})
    if delete_result.deleted_count > 0:
        return jsonify({"message": "Member deleted successfully!"})
    return jsonify({"error": "Member not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
