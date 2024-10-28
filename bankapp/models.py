from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from bankproject import settings
from django.core.exceptions import ObjectDoesNotExist


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, name=None):
        user = self.create_user(email, password, name=name)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email


class Bank(models.Model):
    """Model to represent the bank's total balance."""
    total_balance = models.FloatField(default=0.00)

    @classmethod
    def get_instance(cls):
        """Get the global bank instance. Create if it doesn't exist."""
        try:
            return cls.objects.get(pk=1)
        except ObjectDoesNotExist:
            return cls.objects.create(total_balance=0.00)

    def deposit(self, amount):
        """Method to add funds to the bank's total balance."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")

        self.total_balance += amount
        self.save()

    def withdraw(self, amount):
        """Method to deduct funds from the bank's total balance."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if self.total_balance < amount:
            raise ValueError("Insufficient funds in the bank.")
        self.total_balance -= amount
        self.save()

    def apply_transaction_fee(self, fee):
        """Apply a transaction fee to the bank's balance."""
        if fee <= 0:
            raise ValueError("Transaction fee must be positive.")
        self.deposit(fee)

    def __str__(self):
        return f"Bank Total Balance: {self.total_balance}"


class Account(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="accounts")
    balance = models.FloatField(default=0.00)
    currency = models.CharField(max_length=3, default="NIS")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.name} - {self.currency}"

    def deposit(self, amount):
        """Deposit an amount into the account."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")

        self.balance += amount
        self.save()

    def withdraw(self, amount):
        """Withdraw an amount from the account."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")

        if self.balance >= amount:
            self.balance -= amount
            self.save()
        else:
            raise ValueError("Insufficient balance")

    def close(self):
        """Close the account if balance is non-negative and there are no unpaid loans."""
        if self.balance < 0:
            raise ValueError("Account cannot be closed with a negative balance.")
        if self.loans.filter(paid_off=False).exists():
            raise ValueError("Account cannot be closed with unpaid loans.")
        self.is_active = False
        self.save(update_fields=['is_active'])


from django.core.exceptions import ValidationError


class Transaction(models.Model):

    sender_account = models.ForeignKey(
        'Account', related_name='sent_transactions', null=True, blank=True, on_delete=models.CASCADE
    )
    receiver_account = models.ForeignKey(
        'Account', related_name='received_transactions', null=True, blank=True, on_delete=models.CASCADE
    )
    amount = models.FloatField()
    fee = models.FloatField(default=0)
    transaction_type = models.CharField(max_length=10, default='transfer')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Calculate the fee for the transfer
        self.fee = self.amount * 0.01  # Assuming a 1% transaction fee

        # Ensure that sender and receiver are valid and process the transfer
        if self.transaction_type == 'transfer' and self.sender_account and self.receiver_account:
            if self.sender_account.balance >= self.amount + self.fee:
                # Deduct from sender and add to receiver
                self.sender_account.balance -= (self.amount + self.fee)
                self.receiver_account.balance += self.amount
                self.sender_account.save()
                self.receiver_account.save()

                # Apply the transaction fee to the bank
                bank = Bank.get_instance()
                bank.apply_transaction_fee(self.fee)
            else:
                raise ValueError("Insufficient funds in sender's account for transfer and fee.")

        # Call the original save() to ensure the transaction is recorded
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Transfer of {self.amount} on {self.created_at}"


class Loan(models.Model):
    account = models.ForeignKey('Account', on_delete=models.CASCADE, null=True, related_name='loans')
    amount = models.FloatField()
    interest_rate = models.FloatField()
    term_months = models.IntegerField()
    start_date = models.DateTimeField(default=timezone.now)
    paid_off = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.account.user.name} - {self.amount} at {self.interest_rate}%"
