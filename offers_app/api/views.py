from django.db.models import Min
from django_filters import FilterSet, NumberFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated

from offers_app.api.permissions import IsBusinessUser, IsOfferOwner
from offers_app.api.serializers import (
    OfferdetailsSerializer,
    OffersDetailSerializer,
    OffersListSerializer,
    OffersSerializer,
)
from offers_app.models import Offer, OfferDetail


class OfferListFilter(FilterSet):
    min_price = NumberFilter(field_name="price", lookup_expr="gte")
    max_price = NumberFilter(field_name="price", lookup_expr="lte")


class OffersListCreateView(ListCreateAPIView):
    queryset = Offer.objects.all()
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ["title", "description"]
    filterset_class = OfferListFilter

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        # POST
        return [IsAuthenticated(), IsBusinessUser()]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OffersSerializer
        return OffersListSerializer

    # def get_serializer_context(self):
    #     return {"request": self.request}

    def get_queryset(self):
        return Offer.objects.prefetch_related("details").annotate(
            min_delivery_time=Min("details__delivery_time_in_days"),
            min_price=Min("details__price"),
        )


class OffersDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        # PATCH/DELETE
        return [IsAuthenticated(), IsOfferOwner()]

    def get_serializer_class(self):
        # GET → extended serializer
        if self.request.method == "GET":
            return OffersDetailSerializer
        # PATCH/PUT/DELETE → normal serializer
        return OffersSerializer

    def get_queryset(self):
        return Offer.objects.prefetch_related("details").annotate(
            min_delivery_time=Min("details__delivery_time_in_days"),
            min_price=Min("details__price"),
        )


class OfferdetailsView(RetrieveAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferdetailsSerializer
    permission_classes = [IsAuthenticated]
