from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from bankapp.models import Loan, Account

from loan.serializers import LoanSerializer

LOAN_URL = reverse('loan:loan-list')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PrivateLoanApiTests(TestCase):
    """Tests for authenticated loan API requests"""

    def setUp(self):
        self.user = create_user(email='test@example.com', password='password123')
        self.account = Account.objects.create(user=self.user, balance=1000)
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_loans(self):
        """Test retrieving a list of loans"""
        Loan.objects.create(account=self.account, amount=500, interest_rate=5.0, term_months=12)
        Loan.objects.create(account=self.account, amount=200, interest_rate=3.0, term_months=6)

        res = self.client.get(LOAN_URL)

        loans = Loan.objects.all().order_by('-id')
        serializer = LoanSerializer(loans, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_loan(self):
        """Test creating a loan"""
        payload = {'amount': 1000, 'interest_rate': 4.5, 'term_months': 24}
        res = self.client.post(LOAN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
