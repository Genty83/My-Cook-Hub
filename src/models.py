"""
Module containing the base functions and classes used in the project
"""

import math
from src import mongo

#
RECIPE_DATABASE = mongo.db.recipe

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


    @staticmethod
    def check_limit_value(limit) -> int:
        """ """
        if limit is None:
            limit = 5
        return int(limit)

    
    @staticmethod
    def check_page_number(page_num, total_pages) -> int:

        if page_num is None:
            page_num = 1

        # Check for string characters in page number
        if page_num == "<":
            page_num = 1

        if page_num == ">":
            page_num = total_pages

        return int(page_num)
