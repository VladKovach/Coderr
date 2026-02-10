from django.urls import path

from .views import ReviewsDetailView, ReviewsListCreateView

urlpatterns = [
    path("reviews/", ReviewsListCreateView.as_view(), name="reviews-list"),
    path(
        "reviews/<int:id>/",
        ReviewsDetailView.as_view(),
        name="reviews-detail",
    ),
]
