from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

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
        # Password confirmation check
        if attrs["password"] != attrs["repeated_password"]:
            raise serializers.ValidationError(
                {"repeated_password": "Passwords do not match."}
            )
        # Check email uniqueness
        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError(
                {"email": "User with this email already exists."}
            )

        return attrs

    def create(self, validated_data):
        # Remove confirmation field before user creation
        validated_data.pop("repeated_password")
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login
    """

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        print("username = ", username)
        print("password = ", password)
        user = authenticate(
            username=attrs.get("username"),
            password=attrs.get("password"),
        )
        print(user)
        if not user:
            raise serializers.ValidationError("Invalid credentials")

        attrs["user"] = user
        return attrs
