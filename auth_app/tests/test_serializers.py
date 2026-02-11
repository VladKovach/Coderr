from django.test import TestCase

from auth_app.api.serializers import LoginSerializer, RegistrationSerializer


class RegistrationSerializerTest(TestCase):

    def test_invalid_fields(self):
        """
        Ensure validating.
        """
        data = {
            "username": "",
            "email": "wrong",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
            "type": "wrong",
        }

        serializer = RegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())

        self.assertIn("username", serializer.errors)
        self.assertIn("email", serializer.errors)
        self.assertIn("type", serializer.errors)

    def test_passwords_not_match(self):
        """
        Ensure validating.
        """
        data = {
            "username": "exampleUsername",
            "email": "example@mail.de",
            "password": "examplePassword1111",
            "repeated_password": "examplePassword2222",
            "type": "customer",
        }

        serializer = RegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())

        self.assertIn("repeated_password", serializer.errors)


class LoginSerializerTest(TestCase):

    def test_invalid_fields(self):
        """
        Ensure validating.
        """
        data = {"username": "", "password": ""}

        serializer = LoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())

        self.assertIn("username", serializer.errors)
        self.assertIn("password", serializer.errors)
