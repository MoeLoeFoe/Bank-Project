from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from bankapp.models import Transaction, Account
from transaction.serializers import TransactionSerializer
from django.db.models import Q

TRANSACTION_URL = reverse('transaction:transaction-list')


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
        # Create sender and receiver accounts
        sender_account = Account.objects.create(user=self.user, balance=1000)
        receiver_account = Account.objects.create(user=self.user, balance=500)

        # Create transactions for the user
        Transaction.objects.create(sender_account=sender_account, receiver_account=receiver_account, amount=500,
                                   transaction_type='transfer')
        Transaction.objects.create(sender_account=sender_account, receiver_account=receiver_account, amount=200,
                                   transaction_type='transfer')

        # Perform the GET request
        res = self.client.get(TRANSACTION_URL)

        # Get the expected transactions for the user
        transactions = Transaction.objects.filter(
            Q(sender_account__user=self.user) | Q(receiver_account__user=self.user)
        ).order_by('-created_at')

        # Serialize the expected transactions
        serializer = TransactionSerializer(transactions, many=True)

        # Assert the response
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_deposit_transaction(self):
        """Test creating a deposit transaction"""
        payload = {'amount': 100, 'transaction_type': 'deposit', 'sender_account': self.account1.id,'receiver_account':self.account2.id}
        res = self.client.post(TRANSACTION_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.account1.refresh_from_db()
        self.assertEqual(self.account1.balance, 1100)

    def test_create_withdrawal_transaction(self):
        """Test creating a withdrawal transaction"""
        # Make sure to create or use existing accounts for the sender and receiver
        sender_account = Account.objects.create(user=self.user, balance=1000)
        receiver_account = Account.objects.create(user=self.user, balance=500)  # Or a different user account

        payload = {
            'amount': 200,  # Make sure this amount is valid for withdrawal
            'transaction_type': 'withdrawal',
            'sender_account': sender_account.id,  # Add the sender account ID
            'receiver_account': receiver_account.id,  # Add the receiver account ID
        }

        res = self.client.post(TRANSACTION_URL, payload)



        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        transaction = Transaction.objects.get(id=res.data['id'])
        self.assertEqual(transaction.amount, payload['amount'])

    def test_create_transfer_transaction(self):
        """Test creating a transfer transaction between accounts"""

        sender_account = Account.objects.create(user=self.user, balance=1000)
        receiver_account = Account.objects.create(user=self.user, balance=500)

        payload = {
            'amount': 300,
            'transaction_type': 'transfer',
            'sender_account': sender_account.id,
            'receiver_account': receiver_account.id
        }
        res = self.client.post(TRANSACTION_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        sender_account.refresh_from_db()
        receiver_account.refresh_from_db()

        self.assertEqual(sender_account.balance, 700)
        self.assertEqual(receiver_account.balance, 800)
