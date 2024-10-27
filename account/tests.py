from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from bankapp.models import Account

from account.serializers import AccountSerializer

ACCOUNT_URL = reverse('account:account-list')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicAccountApiTests(TestCase):
    """Tests for unauthenticated account API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_authentication_required(self):
        """Test that authentication is required for accessing accounts"""
        res = self.client.get(ACCOUNT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateAccountApiTests(TestCase):
    """Tests for authenticated account API requests"""

    def setUp(self):
        self.user = create_user(email='test@example.com', password='password123')
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_accounts(self):
        """Test retrieving a list of accounts"""
        # Create two accounts for the user
        account1 = Account.objects.create(user=self.user, balance=500)
        account2 = Account.objects.create(user=self.user, balance=1000)

        # Perform the GET request to retrieve accounts
        res = self.client.get(ACCOUNT_URL)

        # Retrieve all accounts for comparison
        accounts = Account.objects.filter(user=self.user).order_by('id')  # Ensure to filter by user
        serializer = AccountSerializer(accounts, many=True)

        # Assert that the status code is correct
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Assert that the returned data matches the serialized data
        self.assertEqual(res.data, serializer.data)

    def test_accounts_limited_to_user(self):
        """Test retrieving accounts is limited to authenticated user"""
        user2 = create_user(email='other@example.com', password='password123')
        Account.objects.create(user=user2, balance=500)
        account = Account.objects.create(user=self.user, balance=1000)

        res = self.client.get(ACCOUNT_URL)

        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['id'], account.id)

    def test_create_account(self):
        """Test creating a new account"""
        payload = {'balance': 500}
        res = self.client.post(ACCOUNT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        account = Account.objects.get(id=res.data['id'])
        self.assertEqual(account.user, self.user)
        self.assertEqual(account.balance, payload['balance'])
