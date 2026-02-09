from django.db.models import Min
from django_filters import FilterSet, NumberFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
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


class OffersPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class OfferListFilter(FilterSet):
    min_price = NumberFilter(lookup_expr="gte")
    max_delivery_time = NumberFilter(
        field_name="details__delivery_time_in_days", lookup_expr="lte"
    )
    creator_id = NumberFilter(field_name="user_id")

    class Meta:
        model = Offer
        fields = ["creator_id", "min_price", "max_delivery_time"]

    def clean(self):
        """
        super().clean() calls the default clean() method of FilterSet, which:

        Converts query params from strings to the proper Python type (e.g., '3' → 3)

        Runs field-level validation (like your NumberFilter)

        Returns a dict of validated and converted values called cleaned_data
        e.g., {'creator_id': 5, 'max_delivery_time': 7}
        """
        cleaned_data = super().clean()

        creator_id = cleaned_data.get("creator_id")
        if creator_id is not None and not creator_id.is_integer():
            raise ValidationError({"creator_id": "Must be an integer"})

        max_delivery_time = cleaned_data.get("max_delivery_time")
        if (
            max_delivery_time is not None
            and not max_delivery_time.is_integer()
        ):
            raise ValidationError({"max_delivery_time": "Must be an integer"})

        return cleaned_data


class OffersListCreateView(ListCreateAPIView):
    queryset = Offer.objects.all()
    pagination_class = OffersPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["updated_at", "min_price"]
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
