""" Main app file: This file is the entry point to the application """

import os
from src import app, mongo
from flask import render_template, redirect, request, session, flash, url_for
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash


# Landing page
@app.route("/")
def home():
    return render_template("home.html")


# Account page 
@app.route("/account", methods=["GET", "POST"])
def account():
    """
    Shows the create account page and form for creating account
    """

    if request.method == "POST":
        # check if username already exists in database
        existing_user = mongo.db.account.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists", "error")
            return redirect(url_for("account"))

        new_user = {
            "frst_name": request.form.get("fname").lower(),
            "last_name": request.form.get("lname").lower(),
            "username": request.form.get("username").lower(),
            "date_of_birth": request.form.get("dob").lower(),
            "email": request.form.get("email").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "my_recipes": []
        }

        mongo.db.account.insert_one(new_user)

        # put the new_user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Account Creation Successful", "success")
        

    return render_template("account.html")



if __name__ == "__main__":
    app.run(
        host = os.environ.get("IP"),
        port = int(os.environ.get("PORT")),
        debug = os.environ.get("DEBUG")
    )