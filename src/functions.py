"""
Module containing the base functions and classes used in the project
"""

import math

class Pagination:
    """ Class to control the pagination of the given database """

    def __init__(self, database, page = 1, page_size = 5):

        self._database = database
        self.page = page
        self.page_size = page_size

        # Check for none type. If true set properties to default value
        if self.page is None:
            self.page = 1

        if self.page_size is None:
            self.page_size = 5

        self.total_records = len(list(self._database.find()))
        self.total_pages = math.ceil(self.total_records / int(self.page_size))

        # Check to send user back to the first page
        if self.page == "<":
            self.page = 1

        # Check to send user to the last page
        if self.page == ">":
            self.page = self.total_pages

        # Convert property into an integer
        self.page = int(self.page)

        # Set skip and limit
        self._skip = int(self.page_size) * (int(self.page) - 1)
        self._limit = int(self.page_size)


    def get_data(self):
        """ Returns a list of the paginated records """

        data = list(self._database.aggregate([
                {'$match': {}}, 
                {'$skip':  self._skip}, 
                {'$limit': self._limit}
            ]))

        self.records = len(data)
        self.start_index = 1 + self._skip
        self.end_index = self.records + self._skip

        return data


    def get_recipes(self, starts_with):
        """ Returns a list of the paginated records """

        data = list(
        self._database.find(
            {"recipe_name": {"$regex": f"^{starts_with}"}}
            ).skip(self._skip).limit(self._limit))

        self.total_records = len(data)
        self.total_pages = math.ceil(self.total_records / int(self.page_size))

        self.start_index = 1 + self._skip
        self.end_index = self.total_records + self._skip

        return data


