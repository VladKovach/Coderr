from django.test import TestCase

from auth_app.api.serializers import RegistrationSerializer


class RegistrationSerializerTest(TestCase):

    def test_invalid_fields(self):
        """
        Ensure validating.
        """
        data = {
            "username": "",
            "email": "wrong",
            "password": "abc123",
            "repeated_password": "wrong",
            "type": "wrong",
        }

        serializer = RegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())

        self.assertIn("username", serializer.errors)
        self.assertIn("email", serializer.errors)
        self.assertIn("repeated_password", serializer.errors)
        self.assertIn("type", serializer.errors)
