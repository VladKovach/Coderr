from rest_framework import serializers

from offers_app.models import Offer, OfferDetail


class OfferdetailsSerializer(serializers.ModelSerializer):
    """
    OfferdetailsSerializer description
    """

    class Meta:
        model = OfferDetail
        fields = [
            "id",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
        ]


class OfferdetailsRefSerializer(serializers.HyperlinkedModelSerializer):
    """
    OfferdetailsRefSerializer description
    """

    url = serializers.HyperlinkedIdentityField(
        view_name="offerdetail-detail",
        lookup_field="id",
    )

    class Meta:
        model = OfferDetail
        fields = ["id", "url"]


class OfferSerializer(serializers.ModelSerializer):
    """
    OfferSerializer description
    """

    details = OfferdetailsSerializer(many=True)

    class Meta:
        model = Offer
        fields = [
            "id",
            "title",
            "image",
            "description",
            "details",
        ]

    def validate_details(self, value):
        """
        Enforce exactly 3 detail objects if POST
        """

        if self.context["request"].method == "POST" and len(value) != 3:
            raise serializers.ValidationError(
                "Exactly 3 detail objects are required: basic, standard, premium."
            )
        else:
            for detail in value:
                if not detail.get("offer_type"):
                    raise serializers.ValidationError(
                        "offer_type field is required"
                    )

        return value

    def update(self, instance, validated_data):
        """Handle nested update for Offerdetails"""
        details_data = validated_data.pop("details", None)

        # Update Offer fields
        instance = super().update(instance, validated_data)

        if details_data is not None:
            for detail in details_data:
                offer_type = detail.get("offer_type")
                offer_detail = instance.details.get(offer_type=offer_type)
                super().update(offer_detail, detail)  # Update Offerdetails f

        return instance

    def create(self, validated_data):
        """Handle offer creation and nested creation for Offerdetails"""
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
    OffersListSerializer description
    """

    min_price = serializers.IntegerField(read_only=True)
    min_delivery_time = serializers.IntegerField(read_only=True)
    details = OfferdetailsRefSerializer(many=True, read_only=True)
    user_details = serializers.SerializerMethodField()

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
            "min_price",
            "min_delivery_time",
            "user_details",
        ]

    def get_user_details(self, obj):
        """Get user details for the offer."""
        return {
            "first_name": obj.user_first_name,
            "last_name": obj.user_last_name,
            "username": obj.user_username,
        }


class OffersDetailSerializer(serializers.ModelSerializer):
    min_price = serializers.IntegerField(read_only=True)
    min_delivery_time = serializers.IntegerField(read_only=True)
    details = OfferdetailsRefSerializer(many=True, read_only=True)

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
            "min_price",
            "min_delivery_time",
        ]
