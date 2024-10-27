from rest_framework import serializers
from bankapp.models import Account, User

class UserSerializer(serializers.ModelSerializer):
    """Serializer for user data related to accounts"""

    class Meta:
        model = User
        fields = ('id', 'email', 'name')
        read_only_fields = ('id',)
        ref_name = 'AccountUserSerializer'

class AccountSerializer(serializers.ModelSerializer):
    """Serializer for the account model."""

    user = UserSerializer(read_only=True)

    class Meta:
        model = Account
        fields = ('id', 'user', 'balance')
        read_only_fields = ('id',)

    def create(self, validated_data):
        """Creates an account for a user."""
        return Account.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Updates account details."""
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
