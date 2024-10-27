from rest_framework import serializers
from bankapp.models import Transaction, Account


class AccountSerializer(serializers.ModelSerializer):
    """Serializer for account-related data in transactions."""

    class Meta:
        model = Account
        fields = ('id', 'balance')
        read_only_fields = ('id',)


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for the transaction model."""

    sender_account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    receiver_account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())

    class Meta:
        model = Transaction
        fields = ('id', 'sender_account', 'receiver_account', 'amount', 'transaction_type', 'created_at')
        read_only_fields = ('id', 'created_at')

    def create(self, validated_data):
        """Creates a transaction and updates account balances."""
        transaction = Transaction.objects.create(**validated_data)

        # Update account balances based on transaction type
        if transaction.transaction_type == 'deposit':
            transaction.sender_account.balance += transaction.amount
        elif transaction.transaction_type == 'withdrawal':
            transaction.sender_account.balance -= transaction.amount
        elif transaction.transaction_type == 'transfer':
            transaction.sender_account.balance -= transaction.amount
            transaction.receiver_account.balance += transaction.amount

        # Save the accounts after updating the balances
        transaction.sender_account.save()
        transaction.receiver_account.save()

        return transaction
