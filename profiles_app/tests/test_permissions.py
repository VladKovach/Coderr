from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from auth_app.factories import UserFactory
from profiles_app.models import Profile


class ProfilePermissionsTests(APITestCase):
    def setUp(self):
        self.user1 = UserFactory()
        self.user2 = UserFactory()
        self.profile1 = Profile.objects.create(user=self.user1)
        self.profile2 = Profile.objects.create(user=self.user2)

    def test_get_not_allowed_if_not_authenticated(self):
        url = reverse("profile-detail", kwargs={"pk": self.user1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_not_allowed_to_update_someones_profile(self):
        self.client.force_authenticate(user=self.user1)
        request_data = {
            "first_name": "Max",
            "last_name": "Mustermann",
            "location": "Berlin",
            "tel": "987654321",
            "description": "Updated business description",
            "working_hours": "10-18",
            "email": "new_email@business.de",
        }
        url = reverse("profile-detail", kwargs={"pk": self.user2.id})
        response = self.client.patch(url, data=request_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
