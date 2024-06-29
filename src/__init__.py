""" Init file for src package """

import os 
from flask import Flask
from flask_pymongo import PyMongo

# Create flask instance
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")