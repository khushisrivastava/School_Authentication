from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token

class AccountsTest(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')
        self.create_url = reverse('account-create')

    def test_create_user(self):
        data = {
                'first_name': 'foobar',
                'last_name': 'foobar',
                'username': 'foobar',
                'email': 'foobar@example.com',
                'password': 'somepassword'
                }

        response = self.client.post(self.create_url , data, format='json')
        user = User.objects.latest('id')
        ...
        token = Token.objects.get(user=user)
        self.assertEqual(response.data['token'], token.key)

    def test_create_user_with_short_password(self):
        data = {
                'first_name': 'foobar',
                'last_name': 'foobar',
                'username': 'foobar',
                'email': 'foobarbaz@example.com',
                'password': 'foo'
        }

        response = self.client.post(self.create_url, data, format=None)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_no_password(self):
        data = {
                'first_name': 'foobar',
                'last_name': 'foobar',
                'username': 'foobar',
                'email': 'foobarbaz@example.com',
                'password': ''
        }

        response = self.client.post(self.create_url, data, format=None)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_no_username(self):
        data = {
                'first_name': 'foobar',
                'last_name': 'foobar',
                'username': '',
                'email': 'foobarbaz@example.com',
                'password': 'foobar'
            }

        response = self.client.post(self.create_url, data, format=None)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_preexisting_username(self):
        data = {
                'first_name': 'foobar',
                'last_name': 'foobar',
                'username': 'testuser',
                'email': 'user@example.com',
                'password': 'testuser'
            }

        response = self.client.post(self.create_url, data, format=None)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_preexisting_email(self):
        data = {
                'first_name': 'foobar',
                'last_name': 'foobar',
                'username': 'testuser2',
                'email': 'test@example.com',
                'password': 'testuser'
            }

        response = self.client.post(self.create_url, data, format=None)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_create_user_with_invalid_email(self):
        data = {
                'first_name': 'foobar',
                'last_name': 'foobar',
                'username': 'foobarbaz',
                'email':  'testing',
                'passsword': 'foobarbaz'
        }


        response = self.client.post(self.create_url, data, format=None)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_create_user_with_no_email(self):
        data = {
                'first_name': 'foobar',
                'last_name': 'foobar',
                'username' : 'foobar',
                'email': '',
                'password': 'foobarbaz'
        }

        response = self.client.post(self.create_url, data, format=None)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)