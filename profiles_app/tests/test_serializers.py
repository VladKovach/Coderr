from django.test import TestCase
from rest_framework.exceptions import ValidationError

from auth_app.factories import UserFactory
from profiles_app.api.serializers import ProfileDetailSerializer
from profiles_app.models import Profile


class ProfileSerializerTest(TestCase):
    def setUp(self):
        self.user = UserFactory(
            username="exampleUsername",
            email="example@mail.de",
            type="business",
        )
        self.profile = Profile.objects.create(user=self.user)

    def test_valid_fields(self):
        valid_data = {
            "first_name": "Max",
            "last_name": "Mustermann",
            "location": "Berlin",
            "tel": "987654321",
            "description": "Updated business description",
            "working_hours": "10-18",
            "email": "new_email@business.de",
        }

        serializer = ProfileDetailSerializer(
            instance=self.profile, data=valid_data, partial=True
        )
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(self.user.id, serializer.data["user"])
        self.assertEqual(self.user.username, serializer.data["username"])
        self.assertEqual(
            valid_data["first_name"], serializer.data["first_name"]
        )
        self.assertEqual(valid_data["last_name"], serializer.data["last_name"])
        self.assertEqual(valid_data["location"], serializer.data["location"])
        self.assertEqual(valid_data["tel"], serializer.data["tel"])
        self.assertEqual(
            valid_data["description"], serializer.data["description"]
        )
        self.assertEqual(
            valid_data["working_hours"], serializer.data["working_hours"]
        )
        self.assertEqual(valid_data["email"], serializer.data["email"])

    def test_invalid_fields(self):

        invalid_data = {
            "tel": "awdaw",
            "working_hours": "19-18",
            "email": "1111",
        }

        serializer = ProfileDetailSerializer(
            instance=self.profile, data=invalid_data, partial=True
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("tel", serializer.errors)
        self.assertIn("working_hours", serializer.errors)
        self.assertIn("email", serializer.errors)
