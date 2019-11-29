import pytest
import requests

import request_class as script

def test_request(monkeypatch):

    given_data = {'products':
                [{'name': 'Coca-cola', 
                'grade': 'e', 
                'description': 'eau gazėifiée, sucre,  - e150d - ', 
                'url': 'https://fr.openfoodfacts.org/produit/5449000267412/coca-cola', 
                'url_img': 'https://static.openfoodfacts.org/images/products/544/900/026/7412/front_fr.36.400.jpg', 
                'category': 'Sodas,Coca'}]
                }
    
    class MockResponse:

        @staticmethod
        def json():
            return given_data

    def mock_api_openfoodfact(*args, **kwargs):       
        return MockResponse()

    monkeypatch.setattr('requests.get', mock_api_openfoodfact)
    food = script.Request('self.url')
    wanted_value = {'name': 'Coca-cola', 
                        'grade': 'e', 
                        'description': 'eau gazėifiée, sucre,  - e150d - ', 
                        'url': 'https://fr.openfoodfacts.org/produit/5449000267412/coca-cola', 
                        'url_img': 'https://static.openfoodfacts.org/images/products/544/900/026/7412/front_fr.36.400.jpg', 
                        'category': 'Sodas,Coca'}
    assert food.request() == wanted_value

'''def  test_return_data():       
    wanted_value = {'name': 'Coca-cola', 
                        'grade': 'e', 
                        'description': 'eau gazėifiée, sucre,  - e150d - ', 
                        'url': 'https://fr.openfoodfacts.org/produit/5449000267412/coca-cola', 
                        'url_img': 'https://static.openfoodfacts.org/images/products/544/900/026/7412/front_fr.36.400.jpg', 
                        'category': 'Bebidas,Bebidas carbonatadas,Sodas,Bebidas no alcohólicas,Bebidas de cola,Bebidas azucaradas'}
    food = script.Request()
    maps.list_clean = given_data
    test_value = maps.return_data()
    assert test_value == wanted_value

error_data = {'results': [], 'status': 'ZERO_RESULTS'}
def  test_request_error(monkeypatch):
    
    class MockResponseError:

        @staticmethod
        def json():
            return error_data

    def mock_api_google_maps_error(*args, **kwargs):       
        return MockResponseError()

    monkeypatch.setattr('requests.get', mock_api_google_maps_error)
    maps = script.Maps()
    assert maps.request('url') == error_data

def  test_return_data_error():       
    wanted_value = (0, 0, "", "", "")
    maps = script.Maps()
    maps.object_json = error_data
    test_value = maps.return_data()
    assert test_value == wanted_value'''