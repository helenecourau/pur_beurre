from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch
from website.models import Category, Product
import website.constants as co


class HomePageTestCase(TestCase):
    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

class MyProductsPageTestCase(TestCase):
    def setUp(self):
        User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

    def test_favorite_page_returns_200_if_connected(self):
        c = Client()
        response = c.post('/connexion', {'username': 'john', 'password': 'johnpassword'})
        response = c.get('/mes-aliments/')
        self.assertEqual(response.status_code, 200)

    def test_favorite_page_returns_302_if_not_connected(self):
        c = Client()
        response = c.get('/mes-aliments/')
        self.assertEqual(response.status_code, 302)

class ResultPageTestCase(TestCase):
    def test_result_page(self):
        c = Client()
        response = c.get('/resultats/', {'query': 'coca'})
        self.assertEqual(response.status_code, 200)

    def test_result_page_error(self):
        c = Client()
        response = c.get('/resultats/', {'query': 'haribo'})
        self.assertEqual(response.status_code, 200)

class SearchPageTestCase(TestCase):
    def test_search_page(self):
        c = Client()
        response = c.get('/recherche/', {'query': 'coca'})
        self.assertEqual(response.status_code, 200)

    def test_result_page_error(self):
        c = Client()
        response = c.get('/recherche/', {'query': 'haribo'})
        self.assertEqual(response.status_code, 200)

class ProductPageTestCase(TestCase):
    def setUp(self):
        Product.objects.create(name_prod="chocolat", 
                                  description="du très bon chocolat", 
                                  grade="A", 
                                  url="https://url.com/", 
                                  url_img="https://url_img.com/",
                                  slug="chocolat-21")

    def test_detail_page_returns_200(self):
        product_id = Product.objects.get(name_prod='chocolat').id
        product_slug = Product.objects.get(name_prod='chocolat').slug
        response = self.client.get(reverse('product_page', args=(product_id, product_slug,)))
        self.assertEqual(response.status_code, 200)

    def test_detail_page_returns_404(self):
        product_id = Product.objects.get(name_prod='chocolat').id + 1
        product_slug = Product.objects.get(name_prod='chocolat').slug
        response = self.client.get(reverse('product_page', args=(product_id, product_slug,)))
        self.assertEqual(response.status_code, 404)

class ConnectPageTestCase(TestCase):
    def setUp(self):
        User.objects.all().delete()
        User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

    def test_displays_connect_page(self):
        response = self.client.get(reverse('connexion'))
        self.assertEqual(response.status_code, 200)

    def test_connect_page_redirects_after_connexion(self):
        c = Client()
        response = c.post('/connexion', {'username': 'john', 'password': 'johnpassword'})
        response = c.get('/mon-compte', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_connect_page_returns_302_if_connected(self):
        c = Client()
        response = c.post('/connexion', {'username': 'john', 'password': 'johnpassword'})
        self.assertEqual(response.status_code, 302)    

    def test_connect_page_returns_200_if_not_valid_username(self):
        c = Client()
        response = c.post('/connexion', {'username': 'john2', 'password': 'johnpassword'})
        self.assertEqual(response.status_code, 200)

    def test_connect_page_returns_200_if_not_valid_password(self):
        c = Client()
        response = c.post('/connexion', {'username': 'john', 'password': 'johnpassword2'})
        self.assertEqual(response.status_code, 200)

class CreateAccountPageTestCase(TestCase):
    def setUp(self):
        User.objects.all().delete()
        User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

    def test_register_page(self):
        c = Client()
        response = c.get('/creer-compte')
        self.assertEqual(response.status_code, 200)

    def test_register_page_returns_302_if_connected(self):
        c = Client()
        response = c.post('/connexion', {'username': 'john', 'password': 'johnpassword'})
        self.assertEqual(response.status_code, 302)    

    def test_register_page_returns_200_if_not_valid_mail(self):
        c = Client()
        response = c.post('/creer-compte', {'first_name': 'john', 'last_name' : 'lennon', 
                                            'username': 'john', 'mail': 'lennon', 'password': 'johnpassword'})
        self.assertEqual(response.status_code, 200)

    def test_register_page_returns_200_if_user_already_exists(self):
        c = Client()
        response = c.post('/creer-compte', {'first_name': 'john', 'last_name' : 'lennon', 
                                            'username': 'john', 'mail': 'lennon@thebeatles.com', 'password': 'johnpassword'})
        self.assertEqual(response.status_code, 200)

    def test_register_success_create_new_user_in_db(self):
        c = Client()
        c.post('/creer-compte', {'first_name': 'john', 'last_name' : 'lennon', 
                                  'username': 'john2', 'mail': 'lennon@thebeatles.com', 'password': 'johnpassword'})
        user = User.objects.get(username="john2")
        self.assertEqual(user.username, "john2")

given_data = {'products':
                [{'name': 'Coca-cola test', 
                'grade': 'e', 
                'description': 'eau gazėifiée, sucre,  - e150d - ', 
                'url': 'https://fr.openfoodfacts.org/produit/5449000267412/coca-cola', 
                'url_img': 'https://static.openfoodfacts.org/images/products/544/900/026/7412/front_fr.36.400.jpg', 
                'category': 'Sodas,Coca'}]
                }
class AccountPageTestCase(TestCase):
    def setUp(self):
        User.objects.all().delete()
        User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

    def test_account_page_if_connected(self):
        c = Client()
        response = c.post('/connexion', {'username': 'john', 'password': 'johnpassword'})
        response = c.get('/mon-compte')
        self.assertEqual(response.status_code, 200)

    def test_account_page_if_not_connected(self):
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 302)

    @patch('requests.get', return_value=given_data)
    def test_request(self, mock_api_call):
        c = Client()
        response = c.post('/connexion', {'username': 'admin', 'password': co.pwd})
        '''response = self.client.get(reverse('account'))'''
        c.post('/mon-compte', )
        product = Product.objects.get(name_prod="Coca-cola test")
        self.assertEqual(product.name_prod, "Coca-cola test")
