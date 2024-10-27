from rest_framework import viewsets,status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from bankapp.models import Loan,Account
from . import serializers


class LoanViewSet(viewsets.ModelViewSet):
    """ViewSet for managing loans"""

    serializer_class = serializers.LoanSerializer
    queryset = Loan.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve loans for authenticated user's accounts, ordered by created_at"""
        accounts = Account.objects.filter(user=self.request.user)
        return self.queryset.filter(account__in=accounts).order_by('-start_date')  # Change to desired ordering

    def perform_create(self, serializer):
        """Create a new loan for the specified account"""
        account_id = self.request.data.get('account_id')  # Get account_id from request data

        try:
            account = Account.objects.get(id=account_id, user=self.request.user)  # Validate account ownership
        except Account.DoesNotExist:
            return Response({"detail": "Account not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer.save(account=account)  # Save the loan with the account