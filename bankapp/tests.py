from django.test import TestCase
from .models import Account
from django.contrib.auth import get_user_model

class AccountModelTest(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='Testpassword123',
            name='Test User'
        )
        self.account = Account.objects.create(user=self.user, balance=1000.00)

    def test_account_creation(self):
        self.assertEqual(self.account.user.email, 'testuser@example.com')
        self.assertEqual(self.account.balance, 1000.00)

    def test_account_update(self):
        self.account.balance += 500.00
        self.account.save()
        self.assertEqual(self.account.balance, 1500.00)
