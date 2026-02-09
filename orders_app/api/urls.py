from django.urls import path

from .views import (
    OrderCompletedCountDetailView,
    OrderCountDetailView,
    OrdersDetailView,
    OrdersListCreateView,
)

urlpatterns = [
    path("orders/", OrdersListCreateView.as_view(), name="orders-list"),
    path(
        "orders/<int:id>/",
        OrdersDetailView.as_view(),
        name="orders-detail",
    ),
    path(
        "order-count/<int:business_user_id>/",
        OrderCountDetailView.as_view(),
        name="order_count-detail",
    ),
    path(
        "completed-order-count/<int:business_user_id>/",
        OrderCompletedCountDetailView.as_view(),
        name="order_completed_count-detail",
    ),
]
