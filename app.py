""" Main app file: This file is the entry point to the application """

import os
from src import app, mongo
from flask import render_template, redirect, request, session, flash, url_for
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from statistics import mean



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


# Sign in page 
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
    Create recipe view:
    Displays the user form for creating a new recipe.
    """
    if request.method == "POST":

        ingredients_lst = []
        for ingredient in request.form.getlist("ingredients[]"):
            if not ingredient.startswith("\r\n"):
                ingredients_lst.append(ingredient)

        steps_lst = []
        for step in request.form.getlist("step_desc[]"):
            if not step.startswith("\r\n"):
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
                "alt": f"Image of {request.form.get("recipe_name")} recipe."
            }

        # New recipe dictionary
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
            "recipe_img": recipe_img,
            "reviews": []
        }
        # Add recipe to db
        mongo.db.recipe.insert_one(new_recipe)
        flash("Recipe Successfully Added", "success")
        return redirect(url_for("create_recipe"))

    return render_template("create_recipe.html")


@app.route("/edit_recipe/<recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    
    """
    Function to allow the user to edit the selected recipe.
    """

    recipe = mongo.db.recipe.find_one({"_id": ObjectId(recipe_id)})

    if request.method == "POST":

        ingredients_lst = []
        for ingredient in recipe["ingredients"]:
            if not ingredient == "":
                ingredients_lst.append(ingredient)

        steps_lst = []
        for step in recipe["method"]:
            if not step == "":
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
                "alt": f"Image of {request.form.get("recipe_name")} recipe."
            }

        # Edited dictionary
        edited_recipe = {
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
        # Update recipe
        mongo.db.recipe.update_one(
            {"_id": ObjectId(recipe_id)}, {'$set': edited_recipe})
        flash("Recipe Successfully Updated", "success")
        
    return render_template("edit_recipe.html", recipe=recipe)


@app.route("/view_recipes", methods=["GET", "POST"])
def view_recipes():
    """ 
    View recipes page. Shows all available recipe cards
    """

    # Variables
    recipes = list(mongo.db.recipe.find())
    user_session = session.get("user")
    reviews = []
    avg_ratings = []
    review_count = []

    # Loop through recipes and add lists of ratings to reviews list
    for index, value in enumerate(recipes):
        lst = []
        for index in value["reviews"]:
            lst.append(index.get("rating"))
        reviews.append(lst)

    
    # Loop through reviews and add values
    #  to avg_ratings list & review_count list
    for review in reviews:
        if review:
            avg_ratings.append(round(mean(review) * 2) / 2)
            review_count.append(len(review))
        else:
            avg_ratings.append(0)
            review_count.append(0)

    if not user_session is None:
        saved_recipes = mongo.db.account.find_one(
            {"username": user_session}).get('my_recipes', [])
    else:
        saved_recipes = []
           

    return render_template(
            "view_recipes.html", recipes=recipes,
            saved_recipes=saved_recipes, avg_ratings=avg_ratings,
            review_count=review_count,current_page=url_for('view_recipes')
            ) 


@app.route("/recipe/<recipe_id>")
def recipe(recipe_id):
    """
    Recipe view: Shows the full recipe
    """ 

    user_session = session.get("user")
    recipe = mongo.db.recipe.find_one({"_id": ObjectId(recipe_id)})
    reviews = list(mongo.db.recipe.find_one(
        {"_id": ObjectId(recipe_id)}).get('reviews'))

    related_recipes = list(
        mongo.db.recipe.find({"$text": {"$search": recipe["recipe_name"]}}))

    similar_meals = list(
        mongo.db.recipe.find({"meal_type": recipe["meal_type"]}).limit(3))

    ratings = []
    if reviews:
        for dct in reviews:
            ratings.append(dct["rating"])
        avg_rating = round(mean(ratings) * 2) / 2
    else:
        avg_rating = 0

    total_reviews = len(ratings)

    if not user_session is None:
        saved_recipes = mongo.db.account.find_one(
            {"username": session["user"]}).get('my_recipes', [])
    else:
        saved_recipes = []

    return  render_template(
        "recipe.html", recipe=recipe,
        recipe_id=recipe_id, avg_rating=avg_rating, 
        total_reviews=total_reviews, 
        saved_recipes=saved_recipes, 
        current_page=url_for('view_recipes', recipe=recipe_id),
        related_recipes=related_recipes, similar_meals=similar_meals,
        reviews=reviews
        )


@app.route("/save_recipe/<recipe_id>", methods=["GET", "POST"])
def save_recipe(recipe_id):
    """
    Function to save the recipe to the users recipes
    """
    if request.method == "POST":
        mongo.db.account.update_one(
            {"username": session["user"]},
            {"$addToSet": {"my_recipes": recipe_id}}
        )
        flash("Recipe Successfully Saved", "success")

    return redirect(request.args.get('current_page'))


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

    return redirect(request.args.get('current_page'))


@app.route("/my_recipes/<username>", methods=["GET", "POST"])
def my_recipes(username):
    """
    
    """
    user = session["user"]
    # grab the session user's username from the database
    username = mongo.db.account.find_one({"username": user})["username"]
    saved_recipes = mongo.db.account.find_one(
        {"username": user}).get('my_recipes', [])
    
    saved_recipe_ids = [ObjectId(x) for x in saved_recipes]
    my_recipes = list(mongo.db.recipe.find({'_id': {'$in': saved_recipe_ids}}))

    if user:
        recipes = list(mongo.db.recipes.find())
        reviews = []
        avg_ratings = []
        review_count = []

        # Loop through recipes and add lists of ratings to reviews list
        for index, value in enumerate(my_recipes):
            lst = []
            for index in value["reviews"]:
                lst.append(index.get("rating"))
            reviews.append(lst)
        
        # Loop through reviews and add values
        #  to avg_ratings list & review_count list
        for review in reviews:
            if review:
                avg_ratings.append(round(mean(review) * 2) / 2)
                review_count.append(len(review))
            else:
                avg_ratings.append(0)
                review_count.append(0)

        print(avg_ratings)

        return render_template(
            "my_recipes.html", username=username, 
            recipes=recipes, my_recipes=my_recipes,
            saved_recipes=saved_recipes, avg_ratings=avg_ratings,
            review_count=review_count
            )

    return redirect(url_for("sign_in"))


@app.route("/search/<recipe_id>", methods=["GET", "POST"])
def search(recipe_id):
    """
    Search function - allows user to search for recipes based on words
    in the name of the recipe.
    """
    search = request.form.get("search")
    recipes = list(mongo.db.recipe.find({"$text": {"$search": search}}))
    recipe = mongo.db.recipe.find_one({"_id": ObjectId(recipe_id)})

    if not recipes:
        
        flash("No Recipe Found!!", "warning")
        return render_template("recipe.html",recipe_id=recipe_id,
        recipe=recipe, recipes=recipes
    )

    return render_template("recipe.html",recipe_id=recipe_id,
        recipe=recipe, recipes=recipes
    )

    
@app.route("/review/<recipe_id>", methods=["GET", "POST"])
def review(recipe_id):
    """
    Function allows the user topost a review on the displayed recipe.
    """

    recipe = mongo.db.recipe.find_one({"_id": ObjectId(recipe_id)})

    if request.method == "POST":

        review = {
            "review_desc": request.form.get("review_desc"),
            "rating": float(request.form.get("rating")),
            "created_by": session["user"]
        }

        mongo.db.recipe.update_one(
            {"_id": ObjectId(recipe_id)},
            {"$addToSet": {"reviews": review}}
        )
        flash("Review Successfully Added!!", "success")


    return render_template(
        "recipe.html", recipe_id=recipe_id, recipe=recipe
        )
    

if __name__ == "__main__":
    app.run(
        host = os.environ.get("IP"),
        port = int(os.environ.get("PORT")),
        debug = os.environ.get("DEBUG")
    )