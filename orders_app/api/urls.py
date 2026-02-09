from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import OrdersListCreateView

urlpatterns = [
    path("orders/", OrdersListCreateView.as_view(), name="orders-list"),
    # path(
    #     "orders/<int:pk>/",
    #     OffersDetailView.as_view(),
    #     name="offers-detail",
    # ),
    # path(
    #     "order-count/<int:business_user_id>/",
    #     OfferdetailsView.as_view(),
    #     name="offerdetail-detail",
    # ),
    # path(
    #     "completed-order-count/<int:business_user_id>/",
    #     OfferdetailsView.as_view(),
    #     name="offerdetail-detail",
    # ),
]
