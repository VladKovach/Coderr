from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated

from orders_app.api.serializers import (
    OrderCreateSerializer,
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

    # def get_serializer_context(self):
    #     return {"request": self.request}

    # def get_queryset(self):
    #     print("self.request.method = ", self.request.method)

    #     pass


# class OrdersDetailView(RetrieveUpdateDestroyAPIView):
#     queryset = Order.objects.all()

#     def get_permissions(self):
#         if self.request.method == "GET":
#             return [IsAuthenticated()]
#         # PATCH/DELETE
#         return [IsAuthenticated()]

#     def get_serializer_class(self):
#         # GET → extended serializer
#         if self.request.method == "GET":
#             return OrdersDetailSerializer
#         # PATCH/PUT/DELETE → normal serializer
#         return OrdersSerializer

#     def get_queryset(self):
#         return Order.objects.prefetch_related("details").annotate(
#             min_delivery_time=Min("details__delivery_time_in_days"),
#             min_price=Min("details__price"),
#         )
