from rest_framework import serializers

from offers_app.models import Offer, OfferDetail


class OfferdetailsSerializer(serializers.ModelSerializer):
    """
    OffersSerializer description
    """

    class Meta:
        model = OfferDetail
        fields = [
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
        ]


class OffersSerializer(serializers.ModelSerializer):
    """
    OffersSerializer description
    """

    details = OfferdetailsSerializer(many=True)

    class Meta:
        model = Offer
        fields = [
            "user",
            "title",
            "image",
            "description",
            "details",
        ]
        read_only_fields = ["user"]

    def create(self, validated_data):
        details_data = validated_data.pop("details")

        # Assign user automatically
        user = self.context["request"].user
        offer = Offer.objects.create(user=user, **validated_data)
        # Create nested OfferDetail objects
        for detail in details_data:
            OfferDetail.objects.create(offer=offer, **detail)

        return offer


class OffersListSerializer(serializers.ModelSerializer):
    """
    OffersSerializer description
    """

    class Meta:
        model = Offer
        fields = [
            "id",
            "user",
            "title",
            "image",
            "description",
            "created_at",
            "updated_at",
            "details",
        ]


class OffersDetailSerializer(OffersListSerializer):
    min_price = serializers.IntegerField(read_only=True)
    min_delivery_time = serializers.IntegerField(read_only=True)

    class Meta(OffersListSerializer.Meta):
        fields = OffersListSerializer.Meta.fields + [
            "min_price",
            "min_delivery_time",
        ]


class OfferdetailsRefSerializer(serializers.HyperlinkedModelSerializer):
    """
    OffersSerializer description
    """

    url = serializers.HyperlinkedIdentityField(view_name="offerdetails")

    class Meta:
        model = Offer
        fields = ["id", "url"]
