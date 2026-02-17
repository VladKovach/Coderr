from django.db.models import F, Min
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
    OfferSerializer,
    OffersListSerializer,
)
from offers_app.models import Offer, OfferDetail


class OffersPagination(PageNumberPagination):
    """Custom pagination class for Offers list view with default page size of 10 and max page size of 100."""

    page_size = 6
    page_size_query_param = "page_size"
    max_page_size = 100


class OfferListFilter(FilterSet):
    """Custom filter class for Offers list view to filter by creator_id, min_price, and max_delivery_time."""

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
    """View for listing all offers and creating a new offer. GET is open to all, POST is restricted to authenticated business users."""

    pagination_class = OffersPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["updated_at", "min_price"]
    filterset_class = OfferListFilter
    lookup_field = "id"

    ALLOWED_QUERY_PARAMS = {
        "creator_id",
        "min_price",
        "max_delivery_time",
        "ordering",
        "search",
        "page",
        "page_size",
    }

    def get_permissions(self):
        """Allow anyone to GET the list of offers, but only authenticated business users can POST a new offer."""
        if self.request.method == "GET":
            return [AllowAny()]
        # POST
        return [IsAuthenticated(), IsBusinessUser()]

    def get_serializer_class(self):
        """Use OffersListSerializer for GET requests and
        OfferSerializer for POST requests."""
        if self.request.method == "POST":
            return OfferSerializer
        return OffersListSerializer

    def get_queryset(self):
        """Validate query parameters and return the appropriate queryset
        for GET and POST requests.
        For GET, annotate with user details and min price/delivery time.
        For POST, just annotate with min price/delivery time.
        """
        unknown = set(self.request.query_params) - self.ALLOWED_QUERY_PARAMS
        if unknown:
            raise ValidationError(
                {
                    "query_params": f"Unknown parameters: {', '.join(sorted(unknown))}"
                }
            )
        if self.request.method == "POST":
            return Offer.objects.prefetch_related("details").annotate(
                min_delivery_time=Min("details__delivery_time_in_days"),
                min_price=Min("details__price"),
            )
        # GET :
        return Offer.objects.prefetch_related("details").annotate(
            min_delivery_time=Min("details__delivery_time_in_days"),
            min_price=Min("details__price"),
            user_first_name=F("user__first_name"),
            user_last_name=F("user__last_name"),
            user_username=F("user__username"),
        )


class OffersDetailView(RetrieveUpdateDestroyAPIView):
    """View for retrieving, updating, or deleting a specific offer.
    GET is open to all, PATCH/DELETE is restricted to the offer owner."""

    queryset = Offer.objects.all()
    lookup_field = "id"

    def get_permissions(self):
        """Allow anyone to GET offer details, but only the offer owner can
        PATCH or DELETE."""
        if self.request.method == "GET":
            return [IsAuthenticated()]
        # PATCH/DELETE
        return [IsAuthenticated(), IsOfferOwner()]

    def get_serializer_class(self):
        """Use OffersDetailSerializer for GET requests and
        OfferSerializer for PATCH/DELETE requests."""
        # GET → extended serializer
        if self.request.method == "GET":
            return OffersDetailSerializer
        # PATCH/PUT/DELETE → normal serializer
        return OfferSerializer

    def get_queryset(self):
        """Annotate the queryset with min price and delivery time for GET requests."""
        return Offer.objects.annotate(
            min_delivery_time=Min("details__delivery_time_in_days"),
            min_price=Min("details__price"),
        )


class OfferdetailsView(RetrieveAPIView):
    """View for retrieving details of a specific offer detail.
    GET is restricted to authenticated users."""

    queryset = OfferDetail.objects.all()
    serializer_class = OfferdetailsSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"
