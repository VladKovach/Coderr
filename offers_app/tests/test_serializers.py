from unittest import TestCase

from auth_app.factories import UserFactory
from offers_app.api.serializers import OfferSerializer


class OfferSerializerTests(TestCase):

    def test_post_serializer_invalid_data(self):

        invalid_data = {
            "title": "",
            "image": "qwdwqd",
            "description": "",
            "details": [
                {
                    "title": "",
                    "revisions": "qwd",
                    "delivery_time_in_days": "qwd",
                    "price": "qwd",
                    "features": "qwd",
                    "offer_type": "qwd",
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
        serializer = OfferSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)
        self.assertIn("image", serializer.errors)
        self.assertIn("description", serializer.errors)
        self.assertIn("details", serializer.errors)
