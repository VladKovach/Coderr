from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from auth_app.factories import UserFactory


class OrderPremissionsTests(APITestCase):

    def setUp(self):
        self.business_user = UserFactory()
        self.customer_user = UserFactory(type="customer")
        # ------ helper POST -------
        self.orders_list_url = reverse("orders-list")
        self.orders_detail_url = reverse("orders-detail", kwargs={"id": 1})

        self.client.force_authenticate(user=self.business_user)
        # ------ helper POST requests -------

        post_offer_url = reverse("offers-list")
        offer_request_data = {
            "title": "Grafikdesign-Paket",
            "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
            "image": None,
            "details": [
                {
                    "title": "Logo Design",
                    "revisions": 3,
                    "delivery_time_in_days": 5,
                    "price": 150,
                    "features": ["Logo Design", "Visitenkarten"],
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
        self.client.post(
            post_offer_url, data=offer_request_data, format="json"
        )

        self.client.force_authenticate(user=self.customer_user)

        order_request_data = {"offer_detail_id": 1}
        self.post_response = self.client.post(
            self.orders_list_url, data=order_request_data, format="json"
        )

        self.client.logout()
        # ------ helper POST requests -------

    def test_user_must_be_authenticated(self):

        get_list_response = self.client.get(self.orders_list_url)
        self.assertEqual(
            get_list_response.status_code, status.HTTP_401_UNAUTHORIZED
        )

        order_count_detail_url = reverse(
            "order_count-detail", kwargs={"business_user_id": 1}
        )
        order_completed_count_detail_url = reverse(
            "order_completed_count-detail", kwargs={"business_user_id": 1}
        )

        get_count_response = self.client.get(order_count_detail_url)
        self.assertEqual(
            get_count_response.status_code, status.HTTP_401_UNAUTHORIZED
        )
        get_completed_count_response = self.client.get(
            order_completed_count_detail_url
        )
        self.assertEqual(
            get_completed_count_response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_only_customer_user_can_create_order(self):
        self.client.force_authenticate(user=self.business_user)
        response = self.client.post(self.orders_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_only_business_can_update_order(self):
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.patch(self.orders_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_only_staff_can_delete_order(self):
        self.client.force_authenticate(user=self.business_user)
        response = self.client.delete(self.orders_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
