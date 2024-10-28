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



