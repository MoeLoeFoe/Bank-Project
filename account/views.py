from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from bankapp.models import Account
from . import serializers
from rest_framework.views import APIView

class AccountViewSet(viewsets.ModelViewSet):
    """ViewSet for managing accounts"""
    TRANSACTION_FEE_PERCENTAGE = 0.01
    serializer_class = serializers.AccountSerializer
    queryset = Account.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve accounts for the authenticated user"""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Creates a new account"""
        serializer.save(user=self.request.user)

    def get_balance(self, request, pk=None):
        """Retrieve the balance of a specific account"""
        try:
            account = self.get_object()
            balance = account.balance
            return Response({'balance': balance}, status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            return Response({'detail': 'Account not found.'}, status=status.HTTP_404_NOT_FOUND)


    def close_account(self, request, pk=None):
        """Close an account by its primary key."""
        account = self.get_object()

        try:
            account.close()
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': 'Account closed successfully.'}, status=status.HTTP_204_NO_CONTENT)