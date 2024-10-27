from rest_framework import serializers
from bankapp.models import Loan


class LoanSerializer(serializers.ModelSerializer):
    """Serializer for the loan model."""

    class Meta:
        model = Loan
        fields = ('id', 'account', 'amount', 'interest_rate', 'duration_months', 'status', 'created_at')
        read_only_fields = ('id', 'status', 'created_at')

    def create(self, validated_data):
        """Create a loan request."""
        return Loan.objects.create(**validated_data)
