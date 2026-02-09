from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import OfferdetailsView, OffersDetailView, OffersListCreateView

urlpatterns = [
    path("offers/", OffersListCreateView.as_view(), name="offers-list"),
    path(
        "offers/<int:id>/",
        OffersDetailView.as_view(),
        name="offers-detail",
    ),
    path(
        "offerdetails/<int:id>/",
        OfferdetailsView.as_view(),
        name="offerdetail-detail",
    ),
]
