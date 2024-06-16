from flask import Flask
from routes import pages
from pymongo import MongoClient

def create_app():
    app = Flask(__name__)
    app.register_blueprint(pages)
    client = MongoClient("mongodb://localhost:27017/")
    app.db = client.todo
    return app