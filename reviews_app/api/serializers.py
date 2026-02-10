from django.contrib.auth import get_user_model
from rest_framework import serializers

from reviews_app.models import Review

User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer description
    """

    business_user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )

    class Meta:
        model = Review
        fields = [
            "id",
            "business_user",
            "reviewer",
            "rating",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "reviewer"]


class ReviewDetailSerializer(ReviewSerializer):
    class Meta(ReviewSerializer.Meta):
        fields = ReviewSerializer.Meta.fields
        read_only_fields = ReviewSerializer.Meta.read_only_fields + [
            "business_user"
        ]
