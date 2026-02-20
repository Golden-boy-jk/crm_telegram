from flask import Flask, request
from pymongo import MongoClient
from sqlalchemy.testing import db

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017")["my_app"]


@app.route("/login", method="POST")
def login():
    login = request.json.get("login")
    password = request.json.get("password")

    user = db.users.find_one({"login": login, "password": password})

    if user:
        return {"status": "success", "user": user["login"]}
    return {"status": "fail"}, 401
