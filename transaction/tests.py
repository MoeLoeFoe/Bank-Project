from django.test import TestCase
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from bankapp.models import  User,Account

class TransactionTests(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(email='sender@example.com', password='password123')
        self.receiver = User.objects.create_user(email='receiver@example.com', password='password456')
        self.sender_account = Account.objects.create(user=self.sender, balance=1000)
        self.receiver_account = Account.objects.create(user=self.receiver, balance=500)

    def test_create_transaction(self):
        response = self.client.post(reverse('transactions:create'), {
            'sender_account': self.sender_account.id,
            'receiver_account': self.receiver_account.id,
            'amount': 100
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_transaction_fees_applied(self):
        response = self.client.post(reverse('transactions:create'), {
            'sender_account': self.sender_account.id,
            'receiver_account': self.receiver_account.id,
            'amount': 500
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.sender_account.refresh_from_db()
        self.receiver_account.refresh_from_db()
        self.assertEqual(self.sender_account.balance, 495)  # 500 - 5 fee
        self.assertEqual(self.receiver_account.balance, 1000)  # 500 + 500

    def test_transaction_insufficient_funds(self):
        response = self.client.post(reverse('transactions:create'), {
            'sender_account': self.sender_account.id,
            'receiver_account': self.receiver_account.id,
            'amount': 2000  # Exceeding balance
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

