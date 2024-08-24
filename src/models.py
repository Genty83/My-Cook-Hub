"""
Contains the database model classes to access the mongodb collections

CLASSES
--------

==================  ==========================================================
CLASS               DESCRIPTION
==================  ==========================================================
UserAccountModel    Class for managing user accounts
RecipesModel        Class for performing crud actions on recipes
==================  ==========================================================

UserAccountModel
----------------

===================  =========================================================
METHOD               DESCRIPTION
===================  =========================================================
get_saved_recipes    Retrieves the saved recipes from the users account.
remove_saved_recipe  Removes a recipe from the saved recipes list.
add_new_user         Adds a new user to the database.
enter_session        Enters the user into a new session.
===================  =========================================================

RecipesModel
------------

=============================  ===============================================
METHOD                         DESCRIPTION
=============================  ===============================================
get_saved_recipes              Retrieves the saved recipes.
get_similar_recipes            Retrieves a fixed amount of similer recipes.
fetch_records                  Fetches all records from the recipe database.
fetch_records_that_start_with  Gets records that start with a letter.
fetch_my_recipes               Fetches the users recipes.
get_recipe_reviews             Retrieves all the reviews for the given recipe.
get_recipe                     Gets the recipe for the passed in id.
=============================  ===============================================

Static methods
--------------

=============================  ===============================================
METHOD                         DESCRIPTION
=============================  ===============================================
check_limit_value              Checks & converts to int.
check_page_number              Checks & converts the page num to int.
=============================  ===============================================

"""
# Imports
import math
import random

from statistics import mean
from src import mongo
from flask import request, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from typing import Any

# Constants
RECIPE_DATABASE = mongo.db.recipe
ACCOUNT_DATABASE = mongo.db.account

__all__ = [
    "UserAccountModel",
    "RecipesModel"
]


class UserAccountModel:
    """
    Base model for user account database

    Usage
    -----
    >>> user = UserAccountMode(session["user])
    """

    def __init__(self, username: str = None):
        """
        Parameters
        ----------
        username : (str) Defaults to None.
            The session users username.

        Instance properties
        -------------------
        saved_recipes : (list) Defaults to []
            List of users saved recipes
        """
        self.username = username

        # Additional properties
        self.saved_recipes = []

        if self.username is not None:
            self.user_data = ACCOUNT_DATABASE.find_one(
                {"username": self.username.lower()})

    def get_saved_recipes(self) -> list[Any]:
        """
        Gets the users saved recipes from the users account.

        returns : (list)
        """

        if self.username is None:
            return
        else:
            self.saved_recipes = self.user_data.get('my_recipes', [])
        return self.saved_recipes

    def remove_saved_recipe(self, recipe_id):
        """ Removes a saved recipe from the database """

        if request.method == "POST":
            ACCOUNT_DATABASE.update_one(
                {"username": self.username},
                {"$pull": {"my_recipes": recipe_id}}
            )
            flash("Recipe Successfully Removed From Your Recipes!!", "info")

    def add_new_user(self):
        """ Adds a new user to the account database """

        new_user = {
            "first_name": request.form.get("fname").lower(),
            "last_name": request.form.get("lname").lower(),
            "username": request.form.get("username").lower(),
            "date_of_birth": request.form.get("dob").lower(),
            "email": request.form.get("email").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "my_recipes": [],
            "subscribed": False
        }
        flash("Account Creation Successful", "success")

        return ACCOUNT_DATABASE.insert_one(new_user)

    def enter_session(self):
        """ Enters the user into a session """

        if self.user_data:
            # ensure hashed password matches user input
            if check_password_hash(
                    self.user_data["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash(f"Welcome, {request.form.get("username")}", "success")
                return redirect("/")
            else:
                # invalid password match
                flash("Incorrect Username and/or Password", "error")
                return redirect(url_for("sign_in"))
        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password", "error")
            return redirect(url_for("sign_in"))


class RecipesModel:
    """ Base model class for the recipe database """

    def __init__(self):
        # Instance properties
        self.all_records = list(RECIPE_DATABASE.find())
        self.total_records = len(self.all_records)
        self.start_index = None
        self.end_index = None
        self.total_pages = None
        self.page_number = None
        self.limit = None
        self.my_recipes = []

    # Methods
    def get_saved_recipes(self, username):
        """ Gets the user saved recipes """

        user = {"username": username}
        saved_recipes = ACCOUNT_DATABASE.find_one(user).get('my_recipes', [])
        self.my_recipes = saved_recipes

        return saved_recipes

    def get_similar_recipes(self, recipe_id, amount):
        """ Get list of meals by relevent meal type """

        recipe = {"meal_type": self.get_recipe(recipe_id)["meal_type"]}
        meals = list(RECIPE_DATABASE.find())

        if (len(meals)) < amount:
            similar_meals = random.sample(meals, len(meals))
        else:
            similar_meals = random.sample(meals, amount)
        return similar_meals

    def fetch_records(self, limit: int | str = 5, page_num: int | str = 1):
        """ Fetches the given amount of records from the database """

        # Check limit for errors
        self.limit = self.check_limit_value(limit)
        # Set the total pages
        self.total_pages = math.ceil(self.total_records / self.limit)
        # Set page number
        self.page_number = self.check_page_number(page_num, self.total_pages)

        skip = self.limit * (self.page_number - 1)
        query = [{'$match': {}}, {'$skip': skip}, {'$limit': self.limit}]
        data = list(RECIPE_DATABASE.aggregate(query))

        self.set_pagination_indexes(skip, data)

        return data

    def fetch_records_that_start_with(
        self, starts_with: str,
            limit: int | str = 5, page_num: int | str = 1):
        """
        Fetches the given amount of records thats starts with a given letter
        """
        query = {"recipe_name": {"$regex": f"^{starts_with}"}}
        self.total_records = len(list(RECIPE_DATABASE.find(query)))

        # Check limit for errors
        self.limit = self.check_limit_value(limit)
        # Set the total pages
        self.total_pages = math.ceil(self.total_records / self.limit)
        # Set page number
        self.page_number = self.check_page_number(page_num, self.total_pages)

        skip = self.limit * (self.page_number - 1)
        data = list(
            RECIPE_DATABASE.find(query).skip(skip).limit(self.limit))

        self.set_pagination_indexes(skip, data)

        return data

    def fetch_my_recipes(
        self, username: str,
            limit: int | str = 5, page_num: int | str = 1):
        """
        Fetches the given amount of records thats starts with a given letter
        """

        saved_recipes = ACCOUNT_DATABASE.find_one(
            {"username": username}).get('my_recipes', [])

        saved_recipe_ids = [ObjectId(x) for x in saved_recipes]

        query = {'_id': {'$in': saved_recipe_ids}}
        self.total_records = len(list(RECIPE_DATABASE.find(query)))

        # Check limit for errors
        self.limit = self.check_limit_value(limit)
        # Set the total pages
        self.total_pages = math.ceil(self.total_records / self.limit)
        # Set page number
        self.page_number = self.check_page_number(page_num, self.total_pages)

        skip = self.limit * (self.page_number - 1)
        data = list(
            RECIPE_DATABASE.find(query).skip(skip).limit(self.limit))

        self.set_pagination_indexes(skip, data)

        return data

    def get_recipe_reviews(self, recipe_id):
        """
        Gets a list of the reviews for the recipe
        """
        self.reviews = list(RECIPE_DATABASE.find_one(
            {"_id": ObjectId(recipe_id)}).get('reviews'))

        self.total_reviews = len(self.reviews)

        return self

    def get_recipe(self, recipe_id):
        """ Returns a recipe object for the given id passed in """
        return RECIPE_DATABASE.find_one({"_id": ObjectId(recipe_id)})

    def set_pagination_indexes(self, skip, data) -> None:
        """
        Sets the start and end indexes for pagination
        """
        self.start_index = 1 + skip
        self.end_index = len(data) + skip

    @staticmethod
    def check_limit_value(limit) -> int:
        """
        Checks for none type on the limit passed in and converts it
        into an integer value
        """
        if limit is None: 
            limit = 5
        return int(limit)

    @staticmethod
    def check_page_number(page_num, total_pages) -> int:
        """
        Static method: checks and converts the page number
        into an integer value
        """
        if page_num == "<" or page_num is None: 
            page_num = 1
        elif page_num == ">": 
            page_num = total_pages

        return int(page_num)
