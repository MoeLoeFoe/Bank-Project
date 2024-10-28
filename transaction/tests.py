from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from bankapp.models import Transaction, Account
from transaction.serializers import TransactionSerializer
from django.db.models import Q

TRANSACTION_URL = reverse('transaction:transaction-list')
TRANSACTION_FEE_PERCENTAGE = 0.01  # Assuming a 1% transaction fee

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PrivateTransactionApiTests(TestCase):
    """Tests for authenticated transaction API requests"""

    def setUp(self):
        self.user = create_user(email='test@example.com', password='password123')
        self.account1 = Account.objects.create(user=self.user, balance=1000)
        self.account2 = Account.objects.create(user=self.user, balance=500)
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_transactions(self):
        """Test retrieving a list of transactions"""
        sender_account = Account.objects.create(user=self.user, balance=1000)
        receiver_account = Account.objects.create(user=self.user, balance=500)

        Transaction.objects.create(sender_account=sender_account, receiver_account=receiver_account, amount=500,
                                   transaction_type='transfer')
        Transaction.objects.create(sender_account=sender_account, receiver_account=receiver_account, amount=200,
                                   transaction_type='transfer')

        res = self.client.get(TRANSACTION_URL)

        transactions = Transaction.objects.filter(
            Q(sender_account__user=self.user) | Q(receiver_account__user=self.user)
        ).order_by('-created_at')

        serializer = TransactionSerializer(transactions, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


