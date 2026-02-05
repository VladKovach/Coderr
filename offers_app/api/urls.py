from django.urls import path

from .views import OfferdetailsView, OffersDetailView, OffersListCreateView

urlpatterns = [
    path("offers/", OffersListCreateView.as_view(), name="offers-list"),
    path(
        "offers/<int:pk>/",
        OffersDetailView.as_view(),
        name="offers-detail",
    ),
    path(
        "offerdetails/<int:pk>/",
        OfferdetailsView.as_view(),
        name="offerdetails",
    ),
]
