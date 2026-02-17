from unittest import TestCase

from orders_app.api.serializers import OrderDetailSerializer


class OrderDetailSerializerTests(TestCase):

    def test_update_serializer_with_invalid_data(self):

        invalid_data = {"status": "wrong"}
        serializer = OrderDetailSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("status", serializer.errors)
