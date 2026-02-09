from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework.test import APITestCase

from profiles_app.models import Profile

# Create your tests here.
User = get_user_model()


class ProfileModelTestHappy(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="max", password="pass")
        self.profile = Profile(user=self.user, working_hours="11-18")

    # def test_get_profile(self):
    #     url = reverse()
    def test_working_hours_valid(self):
        self.profile.full_clean()  # should pass


class ProfileModelTestUnHappy(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="max", password="pass")

    def test_working_hours_invalid(self):
        profile = Profile(user=self.user, working_hours="19-18")
        # Test that full_clean() raises a ValidationError
        with self.assertRaises(ValidationError):
            profile.full_clean()
