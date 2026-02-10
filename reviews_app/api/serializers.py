from django.contrib.auth import get_user_model
from rest_framework import serializers

from reviews_app.models import Review

User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
    """
    ReviewSerializer description
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


class ReviewDetailSerializer(serializers.ModelSerializer):
    """
    ReviewDetailSerializer description
    """

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
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "reviewer",
            "business_user",
        ]
