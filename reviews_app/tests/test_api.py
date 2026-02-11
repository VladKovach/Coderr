from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from auth_app.factories import UserFactory
from reviews_app.models import Review


class ReviewTestsHappy(APITestCase):

    def setUp(self):
        user = UserFactory(type="customer")
        self.client.force_authenticate(user)

    def test_create_ok(self):
        """
        Ensure we can create a new model object.
        """
        url = reverse("reviews-list")
        data = {
            "business_user": 2,
            "rating": 4,
            "description": "Alles war toll!",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Review.objects.get().description, "Alles war toll!")
