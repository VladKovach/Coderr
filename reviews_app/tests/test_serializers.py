from unittest import TestCase

from reviews_app.api.serializers import (
    ReviewDetailSerializer,
    ReviewSerializer,
)


class ReviewSerializerTests(TestCase):

    def test_invalid_fields(self):

        invalid_data = {
            "business_user": "qwd",
            "rating": "qwd",
            "description": "",
        }
        serializer = ReviewSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("business_user", serializer.errors)
        self.assertIn("rating", serializer.errors)
        self.assertIn("description", serializer.errors)


class ReviewDetailSerializerTests(TestCase):

    def test_invalid_fields(self):

        invalid_data = {
            "rating": "qwd",
            "description": "",
        }
        serializer = ReviewDetailSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("rating", serializer.errors)
        self.assertIn("description", serializer.errors)
