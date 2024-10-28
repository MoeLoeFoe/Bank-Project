from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user model."""

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}
        ref_name = 'UserSerializer'

    def create(self, validated_data):
        """Create a new user with encrypted password"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user and set the password correctly"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def delete(self, instance):
        """Soft delete the user by deactivating them if there are no active accounts."""
        if instance.accounts.filter(is_active=True).exists():
            raise serializers.ValidationError(
                "User cannot be deleted while having active accounts."
            )

        instance.is_active = False
        instance.save(update_fields=['is_active'])

        return {"detail": "User deactivated successfully."}
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid email or password")

        data['user'] = user
        return data