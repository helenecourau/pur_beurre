import pytest
import requests

import request_class as script

given_data = {'products':
                [{'product_name': 'Coca-cola', 
                'nutrition_grades': 'e', 
                'ingredients_text_debug': 'eau gazėifiée, sucre,  - e150d - ', 
                'url': 'https://fr.openfoodfacts.org/produit/5449000267412/coca-cola', 
                'image_url': 'https://static.openfoodfacts.org/images/products/544/900/026/7412/front_fr.36.400.jpg', 
                'categories': 'Sodas,Coca'}]
                }

def test_request(monkeypatch):
    
    class MockResponse:

        @staticmethod
        def json():
            return given_data

    def mock_api_openfoodfact(*args, **kwargs):       
        return MockResponse()

    monkeypatch.setattr('requests.get', mock_api_openfoodfact)
    food = script.Request('self.url')
    wanted_value = [{'name': 'Coca-cola', 
                        'grade': 'e', 
                        'description': 'eau gazėifiée, sucre,  - e150d - ', 
                        'url': 'https://fr.openfoodfacts.org/produit/5449000267412/coca-cola', 
                        'url_img': 'https://static.openfoodfacts.org/images/products/544/900/026/7412/front_fr.36.400.jpg', 
                        'category': 'Sodas,Coca'}]
    assert food.request() == wanted_value

data_error = {'count': 0, 'page': 1, 'page_size': 1000, 'products': [], 'skip': 0}

def test_request_error(monkeypatch):
    
    class MockResponse:

        @staticmethod
        def json():
            return data_error

    def mock_api_openfoodfact(*args, **kwargs):       
        return MockResponse()

    monkeypatch.setattr('requests.get', mock_api_openfoodfact)
    food = script.Request('self.url')
    wanted_value = []
    assert food.request() == wanted_value

given_value = [{'name': 'Coca-cola', 
                        'grade': 'e', 
                        'description': 'eau gazėifiée, sucre,  - e150d - ', 
                        'url': 'https://fr.openfoodfacts.org/produit/5449000267412/coca-cola', 
                        'url_img': 'https://static.openfoodfacts.org/images/products/544/900/026/7412/front_fr.36.400.jpg', 
                        'category': 'Sodas,Coca'}]

def test_return_data():       
    wanted_value = ([{'name': 'Sodas'}, {'name': 'Coca'}], [{'Sodas': 'Coca-cola'}, {'Coca': 'Coca-cola'}])
    food = script.Request('self.url')
    food.foods = given_value
    assert food.split_category() == wanted_value

data_food_error = []
def test_return_data_error():       
    wanted_value = ([], [])
    food = script.Request('self.url')
    food.foods = data_food_error
    assert food.split_category() == wanted_value
