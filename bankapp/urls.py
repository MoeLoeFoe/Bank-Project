from django.urls import path
from .views import AccountListCreate, TransactionListCreate, LoanListCreate

urlpatterns = [
    path('accounts/', AccountListCreate.as_view(), name='account-list-create'),
    path('transactions/', TransactionListCreate.as_view(), name='transaction-list-create'),
    path('loans/', LoanListCreate.as_view(), name='loan-list-create'),
]
