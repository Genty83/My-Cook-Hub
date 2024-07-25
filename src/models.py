"""
Module containing the base functions and classes used in the project
"""

import math
from statistics import mean
import random
from src import mongo
from flask import request, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId

# Constants
RECIPE_DATABASE = mongo.db.recipe
ACCOUNT_DATABASE = mongo.db.account


class UserAccountModel:
    """ Base model for user account database """ 

    def __init__(self, username: str = None):
        # Instance properties
        self.username = username

        # Additional properties
        if not self.username is None:
            self.user_data = ACCOUNT_DATABASE.find_one(
                {"username": self.username.lower()})

        self.saved_recipes = []


    def get_saved_recipes(self):
        """ Method: Gets the users saved recipes """

        if session.get("user") == self.username:
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
        self.avg_rating = None
        self.total_reviews = None

        self.reviews = []
        self.avg_ratings = []
        self.review_count = []

        # Loop through recipes and add lists of ratings to reviews list
        for index, value in enumerate(self.all_records):
            lst = []
            for index in value["reviews"]:
                lst.append(index.get("rating"))
            self.reviews.append(lst)


        # Loop through reviews and add values
        #  to avg_ratings list & review_count list
        for review in self.reviews:
            if review:
                self.avg_ratings.append(round(mean(review) * 2) / 2)
                self.review_count.append(len(review))
            else:
                self.avg_ratings.append(0)
                self.review_count.append(0)

    # Methods 

    def get_similar_recipes(self, recipe_id, amount):
        """ Get list of meals by relevent meal type """

        recipe = self.get_recipe(recipe_id)
        meals = list(RECIPE_DATABASE.find({"meal_type": recipe["meal_type"]}))
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

        self.start_index = 1 + skip
        self.end_index = len(data) + skip

        return data


    def fetch_records_that_start_with(
        self, starts_with: str, limit: int | str = 5, page_num: int | str = 1):
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

        self.start_index = 1 + skip
        self.end_index = len(data) + skip
        
        return data


    def get_recipe_reviews(self, recipe_id):
        """ """
        self.reviews = list(RECIPE_DATABASE.find_one(
            {"_id": ObjectId(recipe_id)}).get('reviews'))

        ratings = []
        if self.reviews:
            for dct in self.reviews:
                ratings.append(dct["rating"])
            self.avg_rating = round(mean(ratings) * 2) / 2
        else:
            self.avg_rating = 0

        self.total_reviews = len(ratings)

        return self


    def get_recipe(self, recipe_id):
        """ Returns a recipe object for the given id passed in """
        return RECIPE_DATABASE.find_one({"_id": ObjectId(recipe_id)})


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

        if page_num is None:
            page_num = 1

        # Check for string characters in page number
        if page_num == "<":
            page_num = 1

        if page_num == ">":
            page_num = total_pages

        return int(page_num)
