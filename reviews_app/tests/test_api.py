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


# class ReviewCRUDTestsUnHappy(APITestCase):

#     def setUp(self):
#         self.customer_user = UserFactory(type="customer")
#         self.business_user = UserFactory()
#         self.client.force_authenticate(user=self.business_user)
#         # ------ helper POST requests -------

#         post_offer_url = reverse("offers-list")
#         offer_request_data = {
#             "title": "Grafikdesign-Paket",
#             "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
#             "image": None,
#             "details": [
#                 {
#                     "title": "Logo Design",
#                     "revisions": 3,
#                     "delivery_time_in_days": 5,
#                     "price": 150,
#                     "features": ["Logo Design", "Visitenkarten"],
#                     "offer_type": "basic",
#                 },
#                 {
#                     "title": "Standard Design",
#                     "revisions": 5,
#                     "delivery_time_in_days": 7,
#                     "price": 200,
#                     "features": ["Logo Design", "Visitenkarte", "Briefpapier"],
#                     "offer_type": "standard",
#                 },
#                 {
#                     "title": "Premium Design",
#                     "revisions": 10,
#                     "delivery_time_in_days": 10,
#                     "price": 500,
#                     "features": [
#                         "Logo Design",
#                         "Visitenkarte",
#                         "Briefpapier",
#                         "Flyer",
#                     ],
#                     "offer_type": "premium",
#                 },
#             ],
#         }
#         self.post_response = self.client.post(
#             post_offer_url, data=offer_request_data, format="json"
#         )

#         self.client.force_authenticate(user=self.customer_user)

#         post_review_url = reverse("reviews-list")
#         review_request_data = {"offer_detail_id": 1}
#         self.post_response = self.client.post(
#             post_review_url, data=review_request_data, format="json"
#         )
#         # ------ helper POST requests -------

#     def test_post_review_with_invalid_offer_detail_id(self):

#         url = reverse("reviews-list")
#         review_request_data = {"offer_detail_id": 111}
#         post_response = self.client.post(
#             url, data=review_request_data, format="json"
#         )
#         self.assertEqual(
#             post_response.status_code, status.HTTP_400_BAD_REQUEST
#         )
#         self.assertIn("offer_detail_id", post_response.data)

#     def test_patch_review_with_invalid_fields(self):
#         self.client.force_authenticate(user=self.business_user)
#         url = reverse("reviews-detail", kwargs={"id": 1})
#         review_request_data = {"status": "wrong"}
#         post_response = self.client.patch(
#             url, data=review_request_data, format="json"
#         )
#         self.assertEqual(
#             post_response.status_code, status.HTTP_400_BAD_REQUEST
#         )
#         self.assertIn("status", post_response.data)

#     def test_delete_review_with_invalid_id(self):
#         staff = UserFactory(is_staff=True)
#         self.client.force_authenticate(user=staff)
#         url = reverse("reviews-detail", kwargs={"id": 100})
#         post_response = self.client.delete(url)
#         self.assertEqual(post_response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_get_review_count_detail_with_no_existed_user(self):
#         url = reverse("review_count-detail", kwargs={"business_user_id": 21})
#         response = self.client.get(url)

#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_get_review_completed_count_detail_with_no_existed_user(self):
#         url = reverse(
#             "review_completed_count-detail", kwargs={"business_user_id": 21}
#         )
#         response = self.client.get(url)

#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
