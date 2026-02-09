from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from offers_app.models import OfferDetail
from orders_app.models import Order


class OrderCreateSerializer(serializers.ModelSerializer):
    """
    OrderSerializer description
    """

    offer_detail_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "offer_type",
            "created_at",
            "offer_detail_id",
        ]
        read_only_fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
        ]

    def validate(self, attrs):
        offer_detail_id = attrs.get("offer_detail_id")

        try:
            offer_detail = OfferDetail.objects.get(id=offer_detail_id)
        except OfferDetail.DoesNotExist:
            raise serializers.ValidationError(
                {"offer_detail_id": "Invalid OfferDetail ID"}
            )

        self.offer_detail = offer_detail

        return attrs

    def create(self, validated_data):
        offer_detail = self.offer_detail
        request = self.context["request"]

        return Order.objects.create(
            customer_user=request.user,
            business_user=offer_detail.offer.user,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
            status="in_progress",
        )


class OrderListSerializer(serializers.ModelSerializer):
    """
    OrderListSerializer description
    """

    class Meta:
        model = Order
        fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "offer_type",
            "created_at",
            "updated_at",
        ]
