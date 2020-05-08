from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from website.models import Product


class HomePageTestCase(TestCase):
    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)


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


class MyProductsPageTestCase(TestCase):
    def setUp(self):
        User.objects.create_user('helene',
                                 'helene@test.com', 'helenecouraupwd')

        Product.objects.create(name_prod="chocolat",
                               description="du très bon chocolat",
                               grade="A",
                               url="https://url.com/",
                               url_img="https://url_img.com/",
                               slug="chocolat-21")
        product = Product.objects.get(name_prod="chocolat")
        user = User.objects.get(username='helene')
        product.fav.add(user)

    def test_favorite_page_returns_200_if_connected(self):
        c = Client()
        response = c.post('/connexion',
                          {'username': 'helene',
                           'password': 'helenecouraupwd'})
        response = c.get('/mes-aliments/')
        self.assertEqual(response.status_code, 200)

    def test_favorite_page_returns_302_if_not_connected(self):
        c = Client()
        response = c.get('/mes-aliments/')
        self.assertEqual(response.status_code, 302)

    def test_delete_fav(self):
        c = Client()
        c.post('/connexion',
               {'username': 'helene',
                'password': 'helenecouraupwd'})
        product = Product.objects.get(name_prod="chocolat")
        user = User.objects.get(username='helene')
        c.post('/mes-aliments/', {'product_id': product.id})
        self.assertFalse(Product.objects.filter(fav__id=user.id).exists())


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
        response = self.client.get(reverse('product_page',
                                           args=(product_id, product_slug,)))
        self.assertEqual(response.status_code, 200)


class ConnectPageTestCase(TestCase):
    def setUp(self):
        User.objects.all().delete()
        User.objects.create_user('helene',
                                 'helene@test.com', 'helenecouraupwd')

    def test_displays_connect_page(self):
        response = self.client.get(reverse('connexion'))
        self.assertEqual(response.status_code, 200)

    def test_connect_page_redirects_after_connexion(self):
        c = Client()
        response = c.post('/connexion',
                          {'username': 'helene',
                           'password': 'helenecouraupwd'})
        response = c.get('/mon-compte', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_connect_page_returns_302_if_connected(self):
        c = Client()
        response = c.post('/connexion',
                          {'username': 'helene',
                           'password': 'helenecouraupwd'})
        self.assertEqual(response.status_code, 302)

    def test_connect_page_returns_200_if_not_valid_username(self):
        c = Client()
        response = c.post('/connexion',
                          {'username': 'helene2',
                           'password': 'helenecouraupwd'})
        self.assertEqual(response.status_code, 200)

    def test_connect_page_returns_200_if_not_valid_password(self):
        c = Client()
        response = c.post('/connexion',
                          {'username': 'helene',
                           'password': 'helenecouraupwd2'})
        self.assertEqual(response.status_code, 200)


class CreateAccountPageTestCase(TestCase):
    def setUp(self):
        User.objects.all().delete()
        User.objects.create_user('helene',
                                 'helene@test.com',
                                 'helenecouraupwd')

    def test_display_register_page(self):
        c = Client()
        response = c.get('/creer-compte')
        self.assertEqual(response.status_code, 200)

    def test_register_page_returns_302_if_connected(self):
        c = Client()
        response = c.post('/connexion',
                          {'username': 'helene',
                           'password': 'helenecouraupwd'})
        self.assertEqual(response.status_code, 302)

    def test_register_page_returns_200_if_not_valid_mail(self):
        c = Client()
        response = c.post('/creer-compte', {'first_name': 'helene',
                                            'last_name': 'courau',
                                            'username': 'helene',
                                            'mail': 'courau',
                                            'password': 'helenecouraupwd'})
        self.assertEqual(response.status_code, 200)

    def test_register_page_returns_200_if_user_already_exists(self):
        c = Client()
        response = c.post('/creer-compte', {'first_name': 'helene',
                                            'last_name': 'courau',
                                            'username': 'helene',
                                            'mail': 'helene@test.com',
                                            'password': 'helenecouraupwd'})
        self.assertEqual(response.status_code, 200)

    def test_register_success_create_new_user_in_db(self):
        c = Client()
        c.post('/creer-compte', {'first_name': 'helene',
                                 'last_name': 'courau',
                                 'username': 'helene2',
                                 'mail': 'helene@test.com',
                                 'password': 'helenecouraupwd'})
        user = User.objects.get(username="helene2")
        self.assertEqual(user.username, "helene2")


class AccountPageTestCase(TestCase):
    def setUp(self):
        User.objects.all().delete()
        User.objects.create_user('helene',
                                 'helene@test.com',
                                 'helenecouraupwd')
        Product.objects.create(name_prod="chocolat",
                               description="du très bon chocolat",
                               grade="A",
                               url="https://url.com/",
                               url_img="https://url_img.com/",
                               slug="chocolat-21")
        product = Product.objects.get(name_prod="chocolat")
        user = User.objects.get(username='helene')
        product.fav.add(user)

    def test_account_page_if_connected(self):
        c = Client()
        response = c.post('/connexion',
                          {'username': 'helene',
                           'password': 'helenecouraupwd'})
        response = c.get('/mon-compte')
        self.assertEqual(response.status_code, 200)

    def test_account_page_if_not_connected(self):
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 302)

    def test_delete_account(self):
        c = Client()
        user = User.objects.get(username='helene')
        c.post('/connexion',
               {'username': 'helene',
                'password': 'helenecouraupwd'})
        c.post('/mon-compte', {'id': user.id})
        self.assertFalse(User.objects.filter(pk=3).exists())

    def test_delete_fav(self):
        c = Client()
        user = User.objects.get(username='helene')
        c.post('/connexion',
               {'username': 'helene',
                'password': 'helenecouraupwd'})
        c.post('/mon-compte', {'id': user.id})
        self.assertFalse(Product.objects.filter(fav__id=user.id).exists())
