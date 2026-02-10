from rest_framework import generics

from reviews_app.api.serializers import (
    ReviewDetailSerializer,
    ReviewSerializer,
)
from reviews_app.models import Review


class ReviewsListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        """Automatically set reviewer to current user."""
        serializer.save(reviewer=self.request.user)


class ReviewsDetailView(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewDetailSerializer
    lookup_field = "id"
