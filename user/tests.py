from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from bankapp.models import User


class UserTests(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'password': 'password123',
            'name': 'Test User'
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_create_user(self):
        response = self.client.post(reverse('user:create'), {
            'email': 'new_user@example.com',
            'password': 'newpassword123',
            'name': 'New User'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_authentication(self):
        response = self.client.post(reverse('user:token'), {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_update_user(self):
        self.client.login(email=self.user_data['email'], password=self.user_data['password'])
        response = self.client.patch(reverse('user:me'), {'name': 'Updated Name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, 'Updated Name')

    def test_user_update_invalid_password(self):
        self.client.login(email=self.user_data['email'], password=self.user_data['password'])
        response = self.client.patch(reverse('user:me'), {'password': ''})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
