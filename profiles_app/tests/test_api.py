from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate

from auth_app.factories import UserFactory
from profiles_app.models import Profile

User = get_user_model()


class ProfileTestsHappy(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.profile = Profile.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_get_profile(self):
        """
        Ensure we can get a profile.
        """
        url = reverse("profile-detail", kwargs={"pk": self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("user", response.data)
        self.assertIn("username", response.data)
        self.assertIn("first_name", response.data)
        self.assertIn("last_name", response.data)
        self.assertIn("file", response.data)
        self.assertIn("location", response.data)
        self.assertIn("tel", response.data)
        self.assertIn("description", response.data)
        self.assertIn("working_hours", response.data)
        self.assertIn("type", response.data)
        self.assertIn("email", response.data)
        self.assertIn("created_at", response.data)

    def test_patch_profile(self):
        """
        Ensure we can get a profile.
        """
        url = reverse("profile-detail", kwargs={"pk": self.user.id})

        request_data = {
            "first_name": "Max",
            "last_name": "Mustermann",
            "location": "Berlin",
            "tel": "987654321",
            "description": "Updated business description",
            "working_hours": "10-18",
            "email": "new_email@business.de",
        }
        response = self.client.patch(url, request_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["first_name"], request_data["first_name"]
        )
        self.assertEqual(response.data["last_name"], request_data["last_name"])
        self.assertEqual(response.data["location"], request_data["location"])
        self.assertEqual(response.data["tel"], request_data["tel"])
        self.assertEqual(
            response.data["description"], request_data["description"]
        )
        self.assertEqual(
            response.data["working_hours"], request_data["working_hours"]
        )
        self.assertEqual(response.data["email"], request_data["email"])


class ProfileTestsUnHappy(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.profile = Profile.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_patch_profile(self):
        """
        Ensure we can not patch profile with wrong data.
        """
        url = reverse("profile-detail", kwargs={"pk": self.user.id})

        request_data = {
            "first_name": "",
            "last_name": "",
            "location": "111",
            "tel": "qwdwq",
            "description": "Updated business description",
            "working_hours": "19-18",
            "email": "1",
        }
        response = self.client.patch(url, request_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
