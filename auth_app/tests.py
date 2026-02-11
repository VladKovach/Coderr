from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# Create your tests here.


class AuthTest(APITestCase):

    def test_registration_and_login_ok(self):
        """
        Ensure we can registrate.
        """
        registration_url = reverse("registration")
        request_body = {
            "username": "exampleUsername",
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
            "type": "customer",
        }
        registration_response = self.client.post(
            registration_url, request_body, format="json"
        )
        self.assertEqual(
            registration_response.status_code, status.HTTP_201_CREATED
        )
        self.assertIn("token", registration_response.data)
        self.assertIn("username", registration_response.data)
        self.assertIn("email", registration_response.data)
        self.assertIn("user_id", registration_response.data)

        # --------- login ---------
        login_url = reverse("login")
        login_data = {
            "username": "exampleUsername",
            "password": "examplePassword",
        }
        login_response = self.client.post(login_url, login_data, format="json")
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn("token", login_response.data)
        self.assertIn("username", login_response.data)
        self.assertIn("email", login_response.data)
        self.assertIn("user_id", login_response.data)
