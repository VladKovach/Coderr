from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Profile

User = get_user_model()


class ProfileModelTestHappy(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="max", password="pass")

    def test_working_hours_valid(self):
        profile = Profile(user=self.user, working_hours="11-18")
        profile.full_clean()  # should pass


class ProfileModelTestUnHappy(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="max", password="pass")

    def test_working_hours_invalid(self):
        profile = Profile(user=self.user, working_hours="19-18")
        # Test that full_clean() raises a ValidationError
        with self.assertRaises(ValidationError):
            profile.full_clean()
