from urllib.parse import urlencode

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from auth_app.factories import UserFactory
from offers_app.models import Offer


class OfferCRUDTestsHappy(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

        # ------ helper POST -------
        post_url = reverse("offers-list")
        request_data = {
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
        self.post_response = self.client.post(
            post_url, data=request_data, format="json"
        )
        # ------ helper POST -------

    def test_create_offer_ok(self):
        """
        Ensure we can create a new offer.
        """

        expected_valid_response = {
            "id": 1,
            "title": "Grafikdesign-Paket",
            "image": None,
            "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
            "details": [
                {
                    "id": 1,
                    "title": "Basic Design",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 100,
                    "features": ["Logo Design", "Visitenkarte"],
                    "offer_type": "basic",
                },
                {
                    "id": 2,
                    "title": "Standard Design",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 200,
                    "features": ["Logo Design", "Visitenkarte", "Briefpapier"],
                    "offer_type": "standard",
                },
                {
                    "id": 3,
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
        response = self.post_response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Offer.objects.count(), 1)
        self.assertEqual(response.data, expected_valid_response)

    def test_get_offer_ok(self):
        url = reverse("offers-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", response.data)
        self.assertIn("results", response.data)
        self.assertIn("created_at", response.data["results"][0])
        self.assertIn("details", response.data["results"][0])
        self.assertIn("created_at", response.data["results"][0])
        self.assertIn("url", response.data["results"][0]["details"][0])
        self.assertIn("min_price", response.data["results"][0])
        self.assertIn("min_delivery_time", response.data["results"][0])
        self.assertIn("user_details", response.data["results"][0])

    def test_get_offer_detail_ok(self):
        """
        Ensure we can get offer detail .
        """
        url = reverse("offers-detail", kwargs={"id": 1})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("user", response.data)
        self.assertIn("title", response.data)
        self.assertIn("image", response.data)
        self.assertIn("description", response.data)
        self.assertIn("created_at", response.data)
        self.assertIn("updated_at", response.data)
        self.assertIn("details", response.data)
        self.assertIn("url", response.data["details"][0])
        self.assertIn("min_price", response.data)
        self.assertIn("min_delivery_time", response.data)

    def test_patch_offer_ok(self):
        """
        Ensure we can patch  offer.
        """

        url = reverse("offers-detail", kwargs={"id": 1})
        request_data = {
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
        }

        response = self.client.patch(url, data=request_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Grafikdesign-Paket")
        self.assertEqual(len(response.data["details"]), 3)
        self.assertEqual(
            response.data["details"][0]["title"], "Basic Design Updated"
        )

    def test_delete_offer_ok(self):
        """
        Ensure we can delete  offer.
        """
        url = reverse("offers-detail", kwargs={"id": 1})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_offerdetails_detail_ok(self):
        url = reverse("offerdetail-detail", kwargs={"id": 1})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("title", response.data)
        self.assertIn("revisions", response.data)
        self.assertIn("delivery_time_in_days", response.data)
        self.assertIn("price", response.data)
        self.assertIn("features", response.data)
        self.assertIn("offer_type", response.data)


class OfferCRUDTestsUnHappy(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

    def test_create_offer_not_ok(self):
        """
        Ensure we can not create a new offer  with false data.
        """
        post_url = reverse("offers-list")
        request_data = {
            "title": "",
            "description": "",
            "image": "qweqwe",
            "details": [
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
        post_response = self.client.post(
            post_url, data=request_data, format="json"
        )

        self.assertEqual(
            post_response.status_code, status.HTTP_400_BAD_REQUEST
        )
        self.assertNotEqual(Offer.objects.count(), 1)

    def test_get_offer_not_ok(self):
        """
        Ensure we can not get offers with false query params.
        """
        params = {  # not existing params
            "owner_id": "1",
            "max_price": "100",
        }
        url = f"{reverse('offers-list')}?{urlencode(params)}"

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_offer_not_ok(self):
        """
        Ensure we can not patch  offer with false data.
        """

        # ------ helper POST -------
        post_url = reverse("offers-list")
        request_data = {
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
        self.client.post(post_url, data=request_data, format="json")
        # ------ helper POST --------

        url = reverse("offers-detail", kwargs={"id": 1})
        request_data = {
            "title": "",
            "details": [
                {
                    "title": "",
                    "revisions": -1,
                    "delivery_time_in_days": 0,
                    "price": "qwd",
                    "features": ["Logo Design", "Flyer"],
                    "offer_type": "basic",
                }
            ],
        }

        response = self.client.patch(url, data=request_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
