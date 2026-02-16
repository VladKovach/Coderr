from django_filters import FilterSet, NumberFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

from reviews_app.api.permissions import IsCustomerOrReadOnly, IsReviewCreator
from reviews_app.api.serializers import (
    ReviewDetailSerializer,
    ReviewSerializer,
)
from reviews_app.models import Review


class RewiewListFilter(FilterSet):

    class Meta:
        model = Review
        fields = ["business_user_id", "reviewer_id"]

    def clean(self):
        cleaned_data = super().clean()
        business_user_id = cleaned_data.get("business_user_id")
        if business_user_id is not None and not business_user_id.is_integer():
            raise ValidationError({"creator_id": "Must be an integer"})

        reviewer_id = cleaned_data.get("reviewer_id")
        if reviewer_id is not None and not reviewer_id.is_integer():
            raise ValidationError({"max_delivery_time": "Must be an integer"})

        return cleaned_data


class ReviewsListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsCustomerOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = RewiewListFilter
    ordering_fields = ["updated_at", "rating"]

    def perform_create(self, serializer):
        """Automatically set reviewer to current user."""
        serializer.save(reviewer=self.request.user)


class ReviewsDetailView(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewDetailSerializer
    lookup_field = "id"
    permission_classes = [IsAuthenticated, IsReviewCreator]
