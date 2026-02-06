from django.core.serializers import get_serializer
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
)

from offers_app.api.serializers import (
    OfferdetailsSerializer,
    OffersDetailSerializer,
    OffersListSerializer,
    OffersSerializer,
)
from offers_app.models import Offer, OfferDetail


class OffersListCreateView(ListCreateAPIView):
    queryset = Offer.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OffersSerializer
        return OffersListSerializer

    def get_serializer_context(self):
        return {"request": self.request}


class OffersDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()

    def get_serializer_class(self):
        # GET → extended serializer
        if self.request.method == "GET":
            return OffersDetailSerializer
        # PATCH/PUT/DELETE → normal serializer
        return OffersSerializer


class OfferdetailsView(RetrieveAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferdetailsSerializer
