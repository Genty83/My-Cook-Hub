"""
Main app file: This file is the entry point to the application

Functions
---------

home: Renders the home page template
get_started: Renders the get started page.
create_recipe: Renders the create recipe page.
edit_recipe: Renders the edit recipe page.
view_recipes: Renders the view recipes page.
az_recipes: Renders the a-z recipes page.
my_recipes: Renders the my recipes page.
recipe: Renders the full recipe page.
save_recipe: Saves the recipe.
remove_recipe: Removes the recipe from the users saved recipes.
delete_recipe: Deletes the recipe from the database.
review: Adds a user review to the recipe.
account: Renders the create account page.
sign_in: Renders the sign in page.
sign_out: Renders the sign out page.

"""

import os
import random
import math

from datetime import date
from src import app, mongo
from flask import render_template, redirect, request, session, flash, url_for
from bson.objectid import ObjectId
from src.models import RecipesModel, UserAccountModel


# Constants
RECIPE_DB = mongo.db.recipe
ACCOUNT_DB = mongo.db.account


# Landing page
@app.route("/")
def home():
    """ Re-routes to the home page  """

    recipes = list(RECIPE_DB.find())
    most_recent = list(RECIPE_DB.find().sort('_id', -1).limit(2))
    featured = random.sample(recipes, 1)

    if len(recipes) < 4:
        more_recipes = random.sample(recipes, len(recipes))
    else:
        more_recipes = random.sample(recipes, 4)

    return render_template(
        "home.html", more_recipes=more_recipes, most_recent=most_recent,
        featured=featured
        )


# Get Started page
@app.route("/get_started", methods=["GET", "POST"])
def get_started():

    """ Displays the get started page """

    return render_template("get_started.html")


# Create recipe page
@app.route("/create_recipe", methods=["GET", "POST"])
def create_recipe():

    """
    Create recipe view:
    Displays the user form for creating a new recipe.
    """

    if request.method == "POST":

        ingredients_lst = []
        steps_lst = []
        recipe_img = {}

        # Add ingredients to list
        for ingredient in request.form.getlist("ingredients[]"):
            if not ingredient.startswith("\r\n"):
                ingredients_lst.append(ingredient)

        # Add steps to step list
        for step in request.form.getlist("step_desc[]"):
            if not step.startswith("\r\n"):
                steps_lst.append(step)

        # Add image and alt text to image dict
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
            "reviews": [],
            "average_rating": 0
        }
        # Add recipe to db
        RECIPE_DB.insert_one(new_recipe)

        flash("Recipe Successfully Added", "success")
        return redirect(url_for("create_recipe"))

    return render_template("create_recipe.html")


@app.route("/edit_recipe/<recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):

    """
    Function to allow the user to edit the selected recipe.
    """
    recipe_id = recipe_id
    recipe = mongo.db.recipe.find_one({"_id": ObjectId(recipe_id)})
    ingredients_lst = []
    steps_lst = []
    recipe_img = {}

    # Add ingredients to list
    for ingredient in request.form.getlist("ingredients[]"):
        if not ingredient == "":
            ingredients_lst.append(ingredient)

    # Add steps to step list
    for step in request.form.getlist("step_desc[]"):
        if not step == "":
            steps_lst.append(step)

    # Add image and alt text to image dict
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

    if request.method == "POST":

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
        RECIPE_DB.update_one(
            {"_id": ObjectId(recipe_id)}, {'$set': edited_recipe})
        flash("Recipe Successfully Updated", "success")

    return render_template("edit_recipe.html", recipe=recipe)


@app.route("/view_recipes", methods=["GET", "POST"])
def view_recipes():
    """
    View recipes page. Shows all available recipe cards
    """

    # Create models
    recipe_model = RecipesModel()
    account_model = UserAccountModel(session.get("user"))

    # Fetch all recipes
    recipes = recipe_model.fetch_records(
        request.form.get("records_select"),
        request.form.get("page")
    )

    # Get saved recipes
    account_model.get_saved_recipes()

    # Render template
    return render_template(
        "view_recipes.html", recipes=recipes,
        recipe_model=recipe_model, account_model=account_model)


@app.route("/az_recipes/<starts_with>", methods=["GET", "POST"])
def az_recipes(starts_with):

    # Create models
    recipe_model = RecipesModel()
    account_model = UserAccountModel(session.get("user"))
    # Fetch recipes that start with letter
    recipes = recipe_model.fetch_records_that_start_with(
        starts_with,
        request.form.get("records_select"),
        request.form.get("page")
    )
    # Get saved recipes
    account_model.get_saved_recipes()
    # Create list of all letters in alphabet
    letters = [chr(i) for i in range(ord('A'), ord('Z') + 1)]

    # Render template
    return render_template(
        "az_recipes.html", letters=letters, recipes=recipes,
        current_letter=starts_with, recipe_model=recipe_model,
        account_model=account_model)


@app.route("/my_recipes", methods=["GET", "POST"])
def my_recipes():
    """ Shows the users saved recipes """

    # Create models
    recipe_model = RecipesModel()
    account_model = UserAccountModel(session.get("user"))

    saved_recipes = recipe_model.get_saved_recipes(session["user"])
    my_recipes = recipe_model.fetch_my_recipes(
        session.get("user"),
        request.form.get("records_select"),
        request.form.get("page")
    )

    return render_template(
        "my_recipes.html", username=session["user"],
        recipes=recipe_model.all_records, my_recipes=my_recipes,
        recipe_model=recipe_model, account_model=account_model,
        saved_recipes=saved_recipes)


@app.route("/recipe/<recipe_id>")
def recipe(recipe_id):
    """
    Recipe view: Shows the full recipe
    """
    # Create model
    recipe_model = RecipesModel()
    account_model = UserAccountModel(session.get("user"))

    recipe = recipe_model.get_recipe(recipe_id)

    recipe_model.get_recipe_reviews(recipe_id)

    # Get list of meals related to recipe name
    related_recipes = list(
        RECIPE_DB.find({"$text": {"$search": recipe["recipe_name"]}}))

    # Create a dictionary of all required template variables
    template_variables = {
        "recipe": recipe,
        "recipe_id": recipe_id,
        "avg_rating": recipe_model.avg_rating,
        "total_reviews": recipe_model.total_reviews,
        "saved_recipes": account_model.saved_recipes,
        "current_page": url_for('view_recipes'),
        "related_recipes": related_recipes,
        "similar_meals": recipe_model.get_similar_recipes(recipe_id, 3),
        "reviews": recipe_model.reviews
    }

    return render_template("recipe.html", **template_variables)


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
        account = UserAccountModel(session.get("user"))
        account.remove_saved_recipe(recipe_id)

    return redirect(url_for("view_recipes"))


@app.route("/delete_recipe/<recipe_id>", methods=["GET", "POST"])
def delete_recipe(recipe_id):
    """
    Deletes the recipe from the database.
    """

    if request.method == "POST":
        RECIPE_DB.delete_one({"_id": ObjectId(recipe_id)})
        flash("The recipe was successfully deleted!!", "info")

    return redirect(url_for("view_recipes"))


@app.route("/search/<recipe_id>", methods=["GET", "POST"])
def search(recipe_id):
    """
    Search function - allows user to search for recipes based on words
    in the name of the recipe.
    """
    search = request.form.get("search")
    recipes = list(RECIPE_DB.find({"$text": {"$search": search}}))
    recipe = RECIPE_DB.find_one({"_id": ObjectId(recipe_id)})

    if not recipes:

        flash("No Recipe Found!!", "warning")
        return redirect(url_for("recipe", recipe_id=recipe_id))

    return render_template(
        "recipe.html", recipe_id=recipe_id, recipe=recipe, recipes=recipes)


@app.route("/review/<recipe_id>", methods=["GET", "POST"])
def review(recipe_id):
    """
    Function allows the user topost a review on the displayed recipe.
    """

    if request.method == "POST":

        review = {
            "review_desc": request.form.get("review_desc"),
            "rating": float(request.form.get("rating")),
            "created_by": session["user"]
        }

        RECIPE_DB.update_one(
            {"_id": ObjectId(recipe_id)},
            {"$addToSet": {"reviews": review}}
        )
        flash("Review Successfully Added!!", "success")
        # Update average rating
        avg_rating = RecipesModel().get_recipe_reviews(recipe_id).avg_rating
        updated_rating = {"average_rating": avg_rating}

        RECIPE_DB.update_one(
            {"_id": ObjectId(recipe_id)}, {'$set': updated_rating})

    return redirect(url_for("recipe", recipe_id=recipe_id))


# Account page
@app.route("/account", methods=["GET", "POST"])
def account():
    """
    Shows the create account page and form for creating a user account
    """

    if request.method == "POST":
        account_model = UserAccountModel(request.form.get("username"))

        if account_model.user_data:
            flash("Username already exists", "error")
            return redirect(url_for("account"))
        # Add new user
        account_model.add_new_user()

    return render_template("account.html")


# Sign in page
@app.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    """
    Shows the sign-in form and
    functionality to sign the user in.
    """
    if request.method == "POST":
        account_model = UserAccountModel(request.form.get("username").lower())
        account_model.enter_session()
        return redirect(url_for("home"))

    return render_template("sign_in.html")


@app.route("/sign_out")
def sign_out():
    """
    Sign-out function - signs the user out.
    """
    # remove user from session cookies
    flash(f"You have been logged out {session["user"]}", "info")
    session.pop("user")

    return redirect(url_for("sign_in"))


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=os.environ.get("DEBUG")
    )
