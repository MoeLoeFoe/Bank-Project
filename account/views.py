from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from bankapp.models import Account
from . import serializers

class AccountViewSet(viewsets.ModelViewSet):
    """ViewSet for managing accounts"""

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
