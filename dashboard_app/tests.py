from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class BaseInfoTests(APITestCase):
    def test_get_base_info_ok(self):
        """
        Ensure we can get .
        """
        url = reverse("baseinfo")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn("review_count", data)
        self.assertIn("average_rating", data)
        self.assertIn("business_profile_count", data)
        self.assertIn("offer_count", data)
