from urllib.parse import urlencode

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from auth_app.factories import UserFactory


class ReviewCRUDTestsHappy(APITestCase):
    def setUp(self):
        self.customer_user = UserFactory(type="customer")
        self.business_user = UserFactory()
        self.client.force_authenticate(user=self.customer_user)

        self.reviews_list_url = reverse("reviews-list")
        self.reviews_detail_url = reverse("reviews-detail", kwargs={"id": 1})

        # ------------ helper POST --------------
        request_data = {
            "business_user": 2,
            "rating": 4,
            "description": "Alles war toll!",
        }
        self.post_response = self.client.post(
            self.reviews_list_url, data=request_data, format="json"
        )
        # ------------ helper POST --------------

    def test_create_review_ok(self):
        """
        Ensure we can create a new review.
        """

        expected_valid_response = {
            "id": 1,
            "business_user": 2,
            "reviewer": 1,
            "rating": 4,
            "description": "Alles war toll!",
        }

        response = self.post_response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key, expected_value in expected_valid_response.items():
            self.assertIn(key, response.data)
            self.assertEqual(response.data[key], expected_value)

        self.assertIn("created_at", response.data)
        self.assertIn("updated_at", response.data)

    def test_get_reviews_list_ok(self):

        expected_valid_response = [
            {
                "id": 1,
                "business_user": 2,
                "reviewer": 1,
                "rating": 4,
                "description": "Alles war toll!",
            }
        ]

        response = self.client.get(self.reviews_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key, expected_value in expected_valid_response[0].items():
            self.assertIn(key, response.data[0])
            self.assertEqual(response.data[0][key], expected_value)

        self.assertIn("created_at", response.data[0])
        self.assertIn("updated_at", response.data[0])

    def test_patch_review_ok(self):
        """
        Ensure creator can patch  review.
        """

        request_data = {
            "rating": 5,
            "description": "Noch besser als erwartet!",
        }
        expected_valid_response = {
            "id": 1,
            "business_user": 2,
            "reviewer": 1,
            "rating": 5,
            "description": "Noch besser als erwartet!",
        }

        response = self.client.patch(
            self.reviews_detail_url, data=request_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key, expected_value in expected_valid_response.items():
            self.assertIn(key, response.data)
            self.assertEqual(response.data[key], expected_value)

        self.assertIn("created_at", response.data)
        self.assertIn("updated_at", response.data)

    def test_delete_review_ok(self):
        """
        Ensure creator can delete  review.
        """
        response = self.client.delete(self.reviews_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ReviewCRUDTestsUnHappy(APITestCase):
    def setUp(self):
        self.customer_user = UserFactory(type="customer")
        self.business_user = UserFactory()
        self.client.force_authenticate(user=self.customer_user)

        self.reviews_list_url = reverse("reviews-list")
        self.reviews_detail_url = reverse("reviews-detail", kwargs={"id": 1})

    def test_create_review_not_ok(self):
        """
        Ensure we can not create a new review with wrong data.
        """

        request_data = {
            "business_user": 2,
            "rating": -1,
            "description": "",
        }
        post_response = self.client.post(
            self.reviews_list_url, data=request_data, format="json"
        )
        self.assertEqual(
            post_response.status_code, status.HTTP_400_BAD_REQUEST
        )

    def test_get_reviews_list_not_ok(self):
        """
        Ensure we can not get reviews with wrong query params.
        """
        params = {  # not existing params
            "business": "1",
            "order": "100",
        }
        url = f"{self.reviews_list_url}?{urlencode(params)}"

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_review_not_ok(self):
        """
        Ensure creator can not patch  review with wrong data.
        """
        # ------------ helper POST --------------
        request_data = {
            "business_user": 2,
            "rating": 4,
            "description": "Alles war toll!",
        }
        self.post_response = self.client.post(
            self.reviews_list_url, data=request_data, format="json"
        )
        # ------------ helper POST --------------
        request_data = {
            "rating": -1,
            "description": "",
        }

        response = self.client.patch(
            self.reviews_detail_url, data=request_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
