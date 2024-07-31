import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from authorization.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken


class UserProfileViewTestCase(TestCase):
    """ Test module for GET user profile API """

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='testuser1@example.com',
            password='password123'
        )
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client = Client()
        self.url = "http://127.0.0.1:8000/api/v1/profile/"

    def test_get_user_profile_success(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {self.access_token}'
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Success.')

    def test_get_user_profile_not_authenticated(self):
        # Remove authentication
        self.client.defaults['HTTP_AUTHORIZATION'] = ''
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AllUsersViewTestCase(TestCase):
    """ Test module for GET all users API """

    def setUp(self):
        self.admin_user = CustomUser.objects.create_user(
            email='admin22@example.com',
            password='password123',
            is_staff=True
        )
        self.normal_user = CustomUser.objects.create_user(
            email='normal00@example.com',
            password='password123'
        )
        refresh = RefreshToken.for_user(self.admin_user)
        self.access_token = str(refresh.access_token)
        self.client = Client()
        self.url = "http://127.0.0.1:8000/api/v1/users/"

    def test_get_all_users_success(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {self.access_token}'
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Success')

    def test_get_all_users_not_staff(self):
        refresh = RefreshToken.for_user(self.normal_user)
        access_token = str(refresh.access_token)
        self.client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_users_not_authenticated(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = ''
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserDetailViewTestCase(TestCase):
    """ Test module for GET single user API """

    def setUp(self):
        self.admin_user = CustomUser.objects.create_user(
            email='admin99@example.com',
            password='password123',
            is_staff=True
        )
        self.target_user = CustomUser.objects.create_user(
            email='target99@example.com',
            password='password123'
        )
        refresh = RefreshToken.for_user(self.admin_user)
        self.access_token = str(refresh.access_token)
        self.client = Client()
        self.url = f"/api/v1/users/{self.target_user.id}/"

    def test_get_valid_single_user(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {self.access_token}'
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Success')

    def test_get_invalid_single_user(self):
        invalid_url = "/api/v1/users/e172f207-1071-477f-a55d-d218b39b15ae/"
        self.client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {self.access_token}'
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_user_detail_not_authenticated(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = ''
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
