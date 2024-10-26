from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from bankapp.models import  User,Account,Loan


class LoanTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='password123')
        self.account = Account.objects.create(user=self.user, balance=1000)
        self.loan_data = {'user': self.user.id, 'amount': 500, 'interest_rate': 5}

    def test_create_loan(self):
        response = self.client.post(reverse('loans:create'), self.loan_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_repay_loan(self):
        loan = Loan.objects.create(**self.loan_data)
        response = self.client.post(reverse('loans:repay', args=[loan.id]), {'amount': 100})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_loan_not_issued_due_to_existing_debt(self):
        Loan.objects.create(**self.loan_data)
        response = self.client.post(reverse('loans:create'), self.loan_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # Expecting a failure due to existing debt
