from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated

from orders_app.api.serializers import (
    OrderCreateSerializer,
    OrderDetailSerializer,
    OrderListSerializer,
)
from orders_app.models import Order


class OrdersListCreateView(ListCreateAPIView):
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]  # IsCustomerForCreate

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OrderCreateSerializer
        return OrderListSerializer


class OrdersDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer


class OrderCountDetailView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCountSerializer


class OrderCompletedCountDetailView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCompletedCountSerializer
