from flask import Flask, request, jsonify
from flask_cors import CORS
import pymongo
from bson.objectid import ObjectId
import time

app = Flask(__name__)
CORS(app)

mongo_uri = "mongodb://localhost:27017"
client = pymongo.MongoClient(mongo_uri)
db = client["my_database"]
users_collection = db["users"]

@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.json
    if "created_ts" not in data:
        data["created_ts"] = time.time()
    data["last_updated_ts"] = time.time()

    result = users_collection.insert_one(data)
    new_user = users_collection.find_one({"_id": result.inserted_id})
    new_user["_id"] = str(new_user["_id"])
    return jsonify(new_user), 201


@app.route("/api/users", methods=["GET"])
def get_users():
    users = list(users_collection.find())
    for u in users:
        u["_id"] = str(u["_id"])
    return jsonify(users), 200

@app.route("/api/users/<user_id>", methods=["GET"])
def get_user(user_id):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        return jsonify({"error": "User not found"}), 404
    user["_id"] = str(user["_id"])
    return jsonify(user), 200

@app.route("/api/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json
    data["last_updated_ts"] = time.time()
    result = users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": data}
    )
    if result.modified_count == 0:
        return jsonify({"error": "No document updated"}), 404
    updated_user = users_collection.find_one({"_id": ObjectId(user_id)})
    updated_user["_id"] = str(updated_user["_id"])
    return jsonify(updated_user), 200

@app.route("/api/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    result = users_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)
