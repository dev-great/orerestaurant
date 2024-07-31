from django.test import TestCase, Client
from django.urls import reverse
from authorization.models import CustomUser
from menu.models import MenuItem
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase


class MenuItemCreateViewTests(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='admin11@example.com',
            password='password123',
            is_staff=True
        )
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client = APIClient()
        self.url = "/api/v1/menus/create/"

    def test_create_menu_item(self):
        data = {
            'name': 'Sample Menu Item',
            'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit',
            'category': 'drink',
            'price': 10.00,
            'tags': [{'name': 'Tag1'}, {'name': 'Tag2'}]
        }
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.post(self.url, data, format='json')

        # Verify response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Menu successfully created')
        self.assertEqual(response.data['data']['name'], 'Sample Menu Item')
        self.assertEqual(len(response.data['data']['tags']), 2)


class MenuItemEditViewTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='admin@example.com',
            password='password123',
            is_staff=True
        )
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client = APIClient()

        self.menu_item = MenuItem.objects.create(name='Sample Menu Item', description='Lorem ipsum dolor sit amet, consectetur adipiscing elit',
                                                 category='drink',
                                                 price=10.00,)
        self.url = f"/api/v1/menus/edit/{self.menu_item.id}/"

    def test_update_menu_item(self):
        # Prepare request data
        data = {
            'name': 'Updated Menu Item',
            'category': 'food'
        }
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        # Make PATCH request
        response = self.client.patch(self.url, data, format='json')

        # Verify response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Menu successfully updated')
        self.assertEqual(response.data['data']['name'], 'Updated Menu Item')


class GetMenuItemByIDViewTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='admin0@example.com',
            password='password123',
            is_staff=True
        )
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client = APIClient()

        self.menu_item = MenuItem.objects.create(name='Sample Menu Item', description='Lorem ipsum dolor sit amet, consectetur adipiscing elit',
                                                 category='drink',
                                                 price=10.00,)
        self.url = f"/api/v1/menus/{self.menu_item.id}/"

    def test_get_menu_item_by_id(self):
        # Make GET request
        response = self.client.get(self.url)

        # Verify response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Successful')
        self.assertEqual(response.data['data']['name'], 'Sample Menu Item')


class GetAllMenuItemsViewTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='admin1@example.com',
            password='password123',
            is_staff=True
        )
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client = APIClient()
        # Create sample menu items
        MenuItem.objects.create(name='Sample Menu Item 1', description='Lorem ipsum dolor sit amet, consectetur adipiscing elit',
                                category='drink', price=10.00)
        MenuItem.objects.create(name='Sample Menu Item 2', description='Lorem ipsum dolor sit amet, consectetur adipiscing elit',
                                category='drink', price=20.00)

        self.url = f"/api/v1/menus/"

    def test_get_all_menu_items(self):
        self.user = CustomUser.objects.create_user(
            email='admin2@example.com',
            password='password123',
            is_staff=True
        )
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client = APIClient()
        # Make GET request
        response = self.client.get(self.url)

        # Verify response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Successful')
        self.assertEqual(len(response.data['data']), 2)


class GetDiscountedMenuItemsViewTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='admin3@example.com',
            password='password123',
            is_staff=True
        )
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client = APIClient()
        # Create sample menu items
        MenuItem.objects.create(name='Sample Menu Item 1', description='Lorem ipsum dolor sit amet, consectetur adipiscing elit',
                                category='drink', price=20.00, is_discounted=True)
        MenuItem.objects.create(name='Sample Menu Item 2', description='Lorem ipsum dolor sit amet, consectetur adipiscing elit',
                                category='drink', price=20.00, is_discounted=False)
        self.url = f"/api/v1/menus/discounted/"

    def test_get_discounted_menu_items(self):
        # Make GET request
        response = self.client.get(self.url)

        # Verify response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['message'], 'Successfully retrieved discounted menu items.')
        self.assertEqual(len(response.data['data']), 1)


class GetDrinksMenuItemsViewTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='admin4@example.com',
            password='password123',
            is_staff=True
        )
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client = APIClient()
        # Create sample menu items
        MenuItem.objects.create(name='Sample Drink 1', price=20.00, category='drink',
                                description='Lorem ipsum dolor sit amet, consectetur adipiscing elit',)
        MenuItem.objects.create(name='Sample Food 1', price=20.00,  category='food',
                                description='Lorem ipsum dolor sit amet, consectetur adipiscing elit',)
        self.url = f"/api/v1/menus/drinks/"

    def test_get_drinks_menu_items(self):
        # Make GET request
        response = self.client.get(self.url)

        # Verify response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'],
                         'Successfully retrieved drinks menu items.')
        self.assertEqual(len(response.data['data']), 1)
