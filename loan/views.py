from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from bankapp.models import Loan
from . import serializers


class LoanViewSet(viewsets.ModelViewSet):
    """ViewSet for managing loans"""

    serializer_class = serializers.LoanSerializer
    queryset = Loan.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve loans for authenticated user"""
        return self.queryset.filter(account__user=self.request.user)

    def perform_create(self, serializer):
        """Create a new loan for the user's account"""
        serializer.save(account=self.request.user.account)
