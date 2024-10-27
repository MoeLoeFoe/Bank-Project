from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from bankapp.models import Transaction, Account
from . import serializers
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

class TransactionViewSet(viewsets.ModelViewSet):
    """ViewSet for managing transactions"""

    serializer_class = serializers.TransactionSerializer
    queryset = Transaction.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve transactions for authenticated user"""
        return self.queryset.filter(
            Q(sender_account__user=self.request.user) | Q(receiver_account__user=self.request.user)
        ).order_by('-created_at')

    def perform_create(self, serializer):
        """Create a new transaction for the user's accounts"""
        serializer.save()