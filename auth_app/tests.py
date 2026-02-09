from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# Create your tests here.


class UserTests(APITestCase):

    def test_registration_and_login(self):
        """
        Ensure we can registrate.
        """
        registration_url = reverse("registration")
        registration_data = {
            "username": "1",
            "email": "1@1.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
            "type": "business",
        }
        registration_response = self.client.post(
            registration_url, registration_data, format="json"
        )
        self.assertEqual(
            registration_response.status_code, status.HTTP_201_CREATED
        )

        login_url = reverse("login")
        login_data = {"username": "1", "password": "examplePassword"}
        login_response = self.client.post(login_url, login_data, format="json")
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn("token", login_response.data)
