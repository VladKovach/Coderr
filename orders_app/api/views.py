from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from orders_app.api.permissions import IsBusinessOrStaff, IsCustomerForCreate
from orders_app.api.serializers import (
    OrderCreateSerializer,
    OrderDetailSerializer,
    OrderListSerializer,
)
from orders_app.models import Order

User = get_user_model()


class OrdersListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated, IsCustomerForCreate]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OrderCreateSerializer
        return OrderListSerializer


class OrdersDetailView(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated, IsBusinessOrStaff]

    lookup_field = "id"


class OrderCountDetailView(APIView):

    def get(self, request, *args, **kwargs):
        business_user_id = kwargs.get("business_user_id")

        try:  # check if user exist
            User.objects.get(pk=business_user_id)
        except User.DoesNotExist:
            return Response(
                {"detail": "No user found with such id."},
                status=status.HTTP_404_NOT_FOUND,
            )
        # Check if there are any orders for this user
        qs = Order.objects.filter(business_user=business_user_id)
        if not qs.exists():
            return Response(
                {"detail": "No orders found for this business user."},
                status=status.HTTP_404_NOT_FOUND,
            )

        count = qs.filter(status="in_progress").count()
        return Response({"order_count": count})


class OrderCompletedCountDetailView(APIView):
    def get(self, request, *args, **kwargs):
        business_user_id = kwargs.get("business_user_id")

        try:  # check if user exist
            User.objects.get(pk=business_user_id)
        except User.DoesNotExist:
            return Response(
                {"detail": "No user found with such id."},
                status=status.HTTP_404_NOT_FOUND,
            )
        # Check if there are any orders for this user
        qs = Order.objects.filter(business_user=business_user_id)
        if not qs.exists():
            return Response(
                {"detail": "No orders found for this business user."},
                status=status.HTTP_404_NOT_FOUND,
            )

        count = qs.filter(status="completed").count()
        return Response({"completed_order_count": count})
