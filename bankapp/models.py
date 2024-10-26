from django.conf import settings
from django.db import models

class BankAccount(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=3, default='NIS')  # e.g., NIS, USD, EUR
    is_active = models.BooleanField(default=True)  # To check if the account is active

    def __str__(self):
        return f"{self.user.email} - {self.balance} {self.currency}"

class Transaction(models.Model):
    from_account = models.ForeignKey(BankAccount, related_name='sent_transactions', on_delete=models.CASCADE)
    to_account = models.ForeignKey(BankAccount, related_name='received_transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction from {self.from_account} to {self.to_account} of {self.amount} {self.from_account.currency}"

class Loan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)  # Percentage
    repayment_period = models.IntegerField()  # Number of months
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Loan of {self.amount} to {self.user.email} at {self.interest_rate}%"

class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)  # e.g., 'NIS'
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4)  # Fixed exchange rate

    def __str__(self):
        return f"{self.code}: {self.exchange_rate}"
