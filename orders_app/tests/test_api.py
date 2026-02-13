from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from auth_app.factories import UserFactory


class OrderCRUDTestsHappy(APITestCase):
    def setUp(self):
        self.customer_user = UserFactory(type="customer")
        self.business_user = UserFactory()
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
        self.post_response = self.client.post(
            post_offer_url, data=offer_request_data, format="json"
        )

        self.client.force_authenticate(user=self.customer_user)

        post_order_url = reverse("orders-list")
        order_request_data = {"offer_detail_id": 1}
        self.post_response = self.client.post(
            post_order_url, data=order_request_data, format="json"
        )
        # ------ helper POST requests -------

    def test_create_order_ok(self):
        """
        Ensure we can create a new order.
        """

        expected_valid_response = {
            "id": 1,
            "customer_user": 1,
            "business_user": 2,
            "title": "Logo Design",
            "revisions": 3,
            "delivery_time_in_days": 5,
            "price": 150,
            "features": ["Logo Design", "Visitenkarten"],
            "offer_type": "basic",
            "status": "in_progress",
        }
        response = self.post_response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key, expected_value in expected_valid_response.items():
            self.assertIn(key, response.data)
            self.assertEqual(response.data[key], expected_value)

        self.assertIn("created_at", response.data)

    def test_get_orders_list_ok(self):

        expected_valid_response = [
            {
                "id": 1,
                "customer_user": 1,
                "business_user": 2,
                "title": "Logo Design",
                "revisions": 3,
                "delivery_time_in_days": 5,
                "price": 150,
                "features": ["Logo Design", "Visitenkarten"],
                "offer_type": "basic",
                "status": "in_progress",
            }
        ]

        url = reverse("orders-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key, expected_value in expected_valid_response[0].items():
            self.assertIn(key, response.data[0])
            self.assertEqual(response.data[0][key], expected_value)

        self.assertIn("created_at", response.data[0])
        self.assertIn("updated_at", response.data[0])

    def test_patch_order_ok(self):
        """
        Ensure we can patch  order.
        """
        self.client.force_authenticate(user=self.business_user)
        expected_valid_response = {
            "id": 1,
            "customer_user": 1,
            "business_user": 2,
            "title": "Logo Design",
            "revisions": 3,
            "delivery_time_in_days": 5,
            "price": 150,
            "features": ["Logo Design", "Visitenkarten"],
            "offer_type": "basic",
            "status": "completed",
        }

        url = reverse("orders-detail", kwargs={"id": 1})
        request_data = {"status": "completed"}

        response = self.client.patch(url, data=request_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key, expected_value in expected_valid_response.items():
            self.assertIn(key, response.data)
            self.assertEqual(response.data[key], expected_value)

        self.assertIn("created_at", response.data)
        self.assertIn("updated_at", response.data)

    def test_delete_order_ok(self):
        """
        Ensure staff can delete  order.
        """
        staff = UserFactory(is_staff=True)
        self.client.force_authenticate(user=staff)
        url = reverse("orders-detail", kwargs={"id": 1})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_order_count_detail_ok(self):
        url = reverse("order_count-detail", kwargs={"business_user_id": 2})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["order_count"], 1)

    def test_get_order_completed_count_detail_ok(self):
        url = reverse(
            "order_completed_count-detail", kwargs={"business_user_id": 2}
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["completed_order_count"], 0)


class OrderCRUDTestsUnHappy(APITestCase):

    def setUp(self):
        self.customer_user = UserFactory(type="customer")
        self.business_user = UserFactory()
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
        self.post_response = self.client.post(
            post_offer_url, data=offer_request_data, format="json"
        )

        self.client.force_authenticate(user=self.customer_user)

        post_order_url = reverse("orders-list")
        order_request_data = {"offer_detail_id": 1}
        self.post_response = self.client.post(
            post_order_url, data=order_request_data, format="json"
        )
        # ------ helper POST requests -------

    def test_post_order_with_invalid_offer_detail_id(self):

        url = reverse("orders-list")
        order_request_data = {"offer_detail_id": 111}
        post_response = self.client.post(
            url, data=order_request_data, format="json"
        )
        self.assertEqual(
            post_response.status_code, status.HTTP_400_BAD_REQUEST
        )
        self.assertIn("offer_detail_id", post_response.data)

    def test_patch_order_with_invalid_fields(self):
        self.client.force_authenticate(user=self.business_user)
        url = reverse("orders-detail", kwargs={"id": 1})
        order_request_data = {"status": "wrong"}
        post_response = self.client.patch(
            url, data=order_request_data, format="json"
        )
        self.assertEqual(
            post_response.status_code, status.HTTP_400_BAD_REQUEST
        )
        self.assertIn("status", post_response.data)

    def test_delete_order_with_invalid_id(self):
        staff = UserFactory(is_staff=True)
        self.client.force_authenticate(user=staff)
        url = reverse("orders-detail", kwargs={"id": 100})
        post_response = self.client.delete(url)
        self.assertEqual(post_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_order_count_detail_with_no_existed_user(self):
        url = reverse("order_count-detail", kwargs={"business_user_id": 21})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_order_completed_count_detail_with_no_existed_user(self):
        url = reverse(
            "order_completed_count-detail", kwargs={"business_user_id": 21}
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
