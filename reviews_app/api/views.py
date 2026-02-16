from django_filters import FilterSet
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
    """FilterSet for filtering reviews by business_user_id and reviewer_id."""

    class Meta:
        model = Review
        fields = ["business_user_id", "reviewer_id"]

    def clean(self):
        """Validate that business_user_id and reviewer_id are integers if they are provided."""
        cleaned_data = super().clean()
        business_user_id = cleaned_data.get("business_user_id")
        if business_user_id is not None and not business_user_id.is_integer():
            raise ValidationError({"business_user_id": "Must be an integer"})

        reviewer_id = cleaned_data.get("reviewer_id")
        if reviewer_id is not None and not reviewer_id.is_integer():
            raise ValidationError({"reviewer_id": "Must be an integer"})

        return cleaned_data


class ReviewsListCreateView(generics.ListCreateAPIView):
    """View for listing and creating reviews."""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsCustomerOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = RewiewListFilter
    ordering_fields = ["updated_at", "rating"]
    ALLOWED_QUERY_PARAMS = {"business_user_id", "reviewer_id", "ordering"}

    def perform_create(self, serializer):
        """Automatically set reviewer to current user."""
        serializer.save(reviewer=self.request.user)

    def get_queryset(self):
        """Validate query parameters and return the queryset."""
        unknown = set(self.request.query_params) - self.ALLOWED_QUERY_PARAMS

        if unknown:
            raise ValidationError(
                {
                    "query_params": f"Unknown parameters: {', '.join(sorted(unknown))}"
                }
            )

        return super().get_queryset()


class ReviewsDetailView(generics.UpdateAPIView, generics.DestroyAPIView):
    """View for updating and deleting reviews."""

    queryset = Review.objects.all()
    serializer_class = ReviewDetailSerializer
    lookup_field = "id"
    permission_classes = [IsAuthenticated, IsReviewCreator]
