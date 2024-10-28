from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from bankapp.models import Account, Loan
from account.serializers import AccountSerializer

ACCOUNT_URL = reverse('account:account-list')
TRANSACTION_FEE_PERCENTAGE = 0.01
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
        self.account = Account.objects.create(user=self.user, balance=1000)
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_create_account(self):
        """Test creating a new account"""
        payload = {'user': self.user.id, 'balance': 2000}
        res = self.client.post(ACCOUNT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Account.objects.count(), 2)
        self.assertEqual(Account.objects.get(id=res.data['id']).balance, 2000)




