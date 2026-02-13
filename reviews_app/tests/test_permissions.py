from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from auth_app.factories import UserFactory


class ReviewPremissionsTests(APITestCase):

    def setUp(self):
        self.business_user = UserFactory()
        self.customer_user = UserFactory(type="customer")
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
        self.client.logout()

    def test_user_must_be_authenticated(self):

        get_list_response = self.client.get(self.reviews_list_url)
        self.assertEqual(
            get_list_response.status_code, status.HTTP_401_UNAUTHORIZED
        )

        post_response = self.client.post(
            self.reviews_list_url, data={}, format="json"
        )
        self.assertEqual(
            post_response.status_code, status.HTTP_401_UNAUTHORIZED
        )

        patch_response = self.client.patch(
            self.reviews_list_url, data={}, format="json"
        )
        self.assertEqual(
            patch_response.status_code, status.HTTP_401_UNAUTHORIZED
        )

        delete_response = self.client.delete(
            self.reviews_list_url, data={}, format="json"
        )
        self.assertEqual(
            delete_response.status_code, status.HTTP_401_UNAUTHORIZED
        )

    def test_only_customer_user_can_create_review(self):
        self.client.force_authenticate(user=self.business_user)
        response = self.client.post(self.reviews_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_only_creator_can_update_or_delete_review(self):
        self.client.force_authenticate(user=self.business_user)
        patch_response = self.client.patch(self.reviews_detail_url)
        self.assertEqual(patch_response.status_code, status.HTTP_403_FORBIDDEN)

        delete_response = self.client.delete(self.reviews_detail_url)
        self.assertEqual(
            delete_response.status_code, status.HTTP_403_FORBIDDEN
        )
