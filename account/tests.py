from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from bankapp.models import  User,Account


class AccountTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='password123')
        self.account_data = {'user': self.user.id, 'balance': 1000}

    def test_create_account(self):
        response = self.client.post(reverse('accounts:create'), self.account_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_account_balance_update(self):
        account = Account.objects.create(**self.account_data)
        response = self.client.patch(reverse('accounts:update', args=[account.id]), {'balance': 1500})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        account.refresh_from_db()
        self.assertEqual(account.balance, 1500)

    def test_account_delete_with_loans(self):
        account = Account.objects.create(**self.account_data)
        # Simulate having an active loan (not implemented yet)
        response = self.client.delete(reverse('accounts:delete', args=[account.id]))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # Expecting a failure due to loan
