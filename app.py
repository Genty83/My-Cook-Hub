""" Main app file: This file is the entry point to the application """

import os
from src import app, mongo
from flask import render_template, redirect, request, session, flash, url_for
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date



# Landing page
@app.route("/")
def home():
    """ Re-routes to the home page  """
    return render_template("home.html")


# Account page 
@app.route("/account", methods=["GET", "POST"])
def account():
    """
    Shows the create account page and form for creating a user account
    """

    if request.method == "POST":

        user = {"username": request.form.get("username").lower()}

        # check if username already exists in database
        existing_user = mongo.db.account.find_one(user)
        if existing_user:
            flash("Username already exists", "error")
            return redirect(url_for("account"))

        # Create new user
        new_user = {
            "first_name": request.form.get("fname").lower(),
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


# Account page 
@app.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    """
    Shows the sign-in form and
    functionality to sign the user in.
    """
    if request.method == "POST":
        # check if username already exists in database
        existing_user = mongo.db.account.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash(f"Welcome, {request.form.get("username")}", "success")
            else:
                # invalid password match
                flash("Incorrect Username and/or Password", "error")
                return redirect(url_for("sign_in"))
        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password", "error")
            return redirect(url_for("sign_in"))

    return render_template("sign_in.html")


@app.route("/sign_out")
def sign_out():
    """
    Sign-out function - signs the user out.
    """
    # remove user from session cookies
    flash("You have been logged out", "info")
    session.pop("user")
    return redirect(url_for("sign_in"))


@app.route("/create_recipe", methods=["GET", "POST"])
def create_recipe():
    
    """
    Add-Recipe view - shows add-recipe page and
    functionality for adding a recipe.
    """
    if request.method == "POST":

        ingredients_lst = []
        for ingredient in request.form.getlist("ingredients[]"):
            if not ingredient.startswith("\r\n"):
                ingredients_lst.append(ingredient)

        steps_lst = []
        for step in request.form.getlist("step_desc[]"):
            if step.startswith("\r\n"):
                continue
            else:
                steps_lst.append(step)

        recipe_img = {}
        if request.form.get("recipe_img") == "":
            recipe_img = {
                "src": "",
                "alt": ""
            }
        else:
            recipe_img = {
                "src": request.form.get("recipe_img"),
                "alt": "Image of {0} recipe.".format(
                    request.form.get("recipe_name"))
            }

        new_recipe = {
            "recipe_name": request.form.get("recipe_name"),
            "recipe_desc": request.form.get("recipe_desc"),
            "meal_type": request.form.get("meal_type"),
            "servings": request.form.get("servings"),
            "cook_time": request.form.get("cook_time"),
            "prep_time": request.form.get("prep_time"),
            "ingredients": ingredients_lst,
            "method": steps_lst,
            "created_by": session["user"],
            "date": date.today().strftime("%d/%m/%Y"),
            "recipe_img": recipe_img
        }

        mongo.db.recipe.insert_one(new_recipe)
        flash("Recipe Successfully Added", "success")
        return redirect(url_for("create_recipe"))

    return render_template("create_recipe.html")


@app.route("/view_recipes", methods=["GET", "POST"])
def view_recipes():
    """ """
    recipes = list(mongo.db.recipe.find())
    meal_types = mongo.db.meal_types.find()
    user_session = session.get("user")

    if not user_session is None:
        saved_recipes = mongo.db.account.find_one(
            {"username": session["user"]}).get('my_recipes', [])
        return render_template(
            "view_recipes.html", recipes=recipes,
            meal_types=meal_types, saved_recipes=saved_recipes,
            current_page=url_for('view_recipes'))    

    return render_template("view_recipes.html", recipes=recipes) 


@app.route("/recipe/<recipe_id>")
def recipe(recipe_id):
    """ """ 

    recipe = mongo.db.recipe.find_one({"_id": ObjectId(recipe_id)})
    meal_types = mongo.db.meal_types.find()

    user_session = session.get("user")

    if not user_session is None:
        saved_recipes = mongo.db.account.find_one(
            {"username": session["user"]}).get('my_recipes', [])

        return  render_template(
            "recipe.html", recipe=recipe,
            meal_types=meal_types, recipe_id=recipe_id,
            current_page=url_for('view_recipes', recipe=recipe_id))

    return  render_template(
            "recipe.html", recipe=recipe,
            meal_types=meal_types, recipe_id=recipe_id,
            current_page=url_for('view_recipes', recipe_id=recipe_id))



@app.route("/save_recipe/<recipe_id>", methods=["GET", "POST"])
def save_recipe(recipe_id):
    """
    Save-recipe function - saves the recipe to show in
    the 'My CookBook' tab in the user's profile.
    """
    if request.method == "POST":
        mongo.db.account.update_one(
            {"username": session["user"]},
            {"$addToSet": {"my_recipes": recipe_id}}
        )
        flash("Recipe Successfully Saved", "success")

    current_page = request.args.get('current_page')
    return redirect(current_page)


@app.route("/remove_recipe/<recipe_id>", methods=["GET", "POST"])
def remove_recipe(recipe_id):
    """
    Removes the recipe from the users recipe list. 
    """
    if request.method == "POST":
        mongo.db.account.update_one(
            {"username": session["user"]},
            {"$pull": {"my_recipes": recipe_id}}
        )
        flash("Recipe Successfully Removed From Your Recipes!!", "info")

    current_page = request.args.get('current_page')
    return redirect(current_page)


@app.route("/my_recipes/<username>", methods=["GET", "POST"])
def my_recipes(username):
    """
    
    """
    user = session["user"]
    # grab the session user's username from the database
    username = mongo.db.account.find_one(
        {"username": user})["username"]
    saved_recipes = mongo.db.account.find_one(
        {"username": user}).get('my_recipes', [])
    
    saved_recipe_ids = [ObjectId(x) for x in saved_recipes]
    my_recipes = mongo.db.recipe.find({'_id': {'$in': saved_recipe_ids}})

    if user:
        recipes = list(mongo.db.recipes.find())

        return render_template(
            "my_recipes.html", 
            username=username, 
            recipes=recipes, 
            my_recipes=my_recipes,
            saved_recipes=saved_recipes
            )

    return redirect(url_for("sign_in"))



if __name__ == "__main__":
    app.run(
        host = os.environ.get("IP"),
        port = int(os.environ.get("PORT")),
        debug = os.environ.get("DEBUG")
    )