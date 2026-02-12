from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from auth_app.factories import UserFactory
from offers_app.models import Offer


class OfferPremissionsTests(APITestCase):

    def setUp(self):
        self.business_user = UserFactory()
        self.business_user2 = UserFactory()
        self.customer_user = UserFactory(type="customer")
        # ------ helper POST -------
        self.offers_list_url = reverse("offers-list")
        self.offers_detail_url = reverse("offers-detail", kwargs={"id": 1})
        self.offerdetail_detail_url = reverse(
            "offerdetail-detail", kwargs={"id": 1}
        )

        self.post_request_data = {
            "title": "Grafikdesign-Paket",
            "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
            "image": None,
            "details": [
                {
                    "title": "Basic Design",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 100,
                    "features": ["Logo Design", "Visitenkarte"],
                    "offer_type": "basic",
                },
                {
                    "title": "Standard Design",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 200,
                    "features": ["Logo Design", "Visitenkarte", "Briefpapier"],
                    "offer_type": "standard",
                },
                {
                    "title": "Premium Design",
                    "revisions": 10,
                    "delivery_time_in_days": 10,
                    "price": 500,
                    "features": [
                        "Logo Design",
                        "Visitenkarte",
                        "Briefpapier",
                        "Flyer",
                    ],
                    "offer_type": "premium",
                },
            ],
        }

    def test_no_authentication_get_offers_list_ok(self):
        """
        Ensure we can get with no authentication list.
        """

        response = self.client.get(self.offers_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_only_business_user_can_create_offer(self):
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.post(self.offers_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_must_be_authenticated(self):

        response = self.client.get(self.offers_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(self.offerdetail_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_only_creator_can_update_or_delete_offer(self):
        self.client.force_authenticate(user=self.business_user)
        self.client.post(
            self.offers_list_url, data=self.post_request_data, format="json"
        )
        self.client.logout()
        self.client.force_authenticate(user=self.business_user2)
        patch_response = self.client.patch(
            self.offers_detail_url,
            data={
                "title": "Updated Grafikdesign-Paket",
                "details": [
                    {
                        "title": "Basic Design Updated",
                        "revisions": 3,
                        "delivery_time_in_days": 6,
                        "price": 120,
                        "features": ["Logo Design", "Flyer"],
                        "offer_type": "basic",
                    }
                ],
            },
            format="json",
        )
        self.assertEqual(patch_response.status_code, status.HTTP_403_FORBIDDEN)

        delete_response = self.client.delete(self.offers_detail_url)
        self.assertEqual(
            delete_response.status_code, status.HTTP_403_FORBIDDEN
        )
