from rest_framework import serializers
from bankapp.models import Loan


class LoanSerializer(serializers.ModelSerializer):
    """Serializer for the loan model."""

    class Meta:
        model = Loan
        fields = ('id', 'account', 'amount', 'interest_rate', 'term_months', 'start_date', 'paid_off')
        read_only_fields = ('id', 'paid_off', 'start_date')

    def create(self, validated_data):
        """Create a loan request."""
        return Loan.objects.create(**validated_data)
