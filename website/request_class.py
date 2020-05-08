import requests
import re

from . import constants


class Request:
    '''Requests and parses data from the OpenFoodFact API'''

    def __init__(self, cat):
        self.cat = cat
        self.url = constants.general + constants.research\
            + self.cat + constants.format_research
        # this is the list used by the other classes
        self.foods, self.duplicate_entries = [], []

    def request(self):
        '''Requests and parses data from the OpenFoodFact API'''
        object_json = requests.get(self.url).json()
        list_clean = object_json['products']
        # the object json from the API
        # has a lot of data and we only need the data from product
        for dico in list_clean:  # this loop screens the dict in the list and
            # put the info we need in a dico and each dico in self.foods list
            if dico.get("image_url") and dico.get("categories")\
                and dico.get("product_name")\
                and dico.get("nutrition_grades")\
                    and dico.get("ingredients_text_debug"):
                # we take only the product with url,
                # category and nutrition grade
                # because we need all those fields
                info_product = {
                    "name": dico["product_name"].capitalize().strip(),
                    "grade": dico["nutrition_grades"],
                    "description": dico["ingredients_text_debug"],
                    "url": dico["url"],
                    "url_img": dico["image_url"],
                    "category": dico["categories"],
                    }
                if info_product["name"] not in self.duplicate_entries:
                    self.duplicate_entries.append(info_product["name"])
                    self.foods.append(info_product)
        return self.foods

    def split_category(self):
        '''Splits the store string in list values and maintains
        the link between each category and the products.'''
        self.category, self.unique_category, duplicate_entries = [], [], []
        for i, first_value in enumerate(self.foods):
            categories_product = {"name": first_value["category"]}
            for key_category, value_category in categories_product.items():
                value_category = re.sub(", ", ",", value_category)
                value_category = value_category.split(',')
            for i, final_value in enumerate(value_category):
                categories = {"name": final_value.capitalize()}
                unique_category = {final_value.capitalize():
                                   first_value["name"]}
                self.unique_category.append(unique_category)  # this list
                # is used to create the lists for the intermediate tables
                if categories["name"] not in duplicate_entries:
                    duplicate_entries.append(categories["name"])
                    # this list is used to insert stores in the database
                    self.category.append(categories)
        return self.category, self.unique_category
