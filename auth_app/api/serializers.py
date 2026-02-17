from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

from profiles_app.models import Profile

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer description
    """

    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "username", "password", "repeated_password", "type")
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        """Password confirmation check and email uniqueness check"""
        if attrs["password"] != attrs["repeated_password"]:
            raise serializers.ValidationError(
                {"repeated_password": "Passwords do not match."}
            )

        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError(
                {"email": "User with this email already exists."}
            )

        return attrs

    def create(self, validated_data):
        """Create a new user and associated profile."""
        validated_data.pop("repeated_password")
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user)
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login
    """

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """Authenticate user with provided credentials."""
        user = authenticate(
            username=attrs.get("username"),
            password=attrs.get("password"),
        )

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        attrs["user"] = user
        return attrs
