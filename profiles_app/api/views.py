from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from profiles_app.models import Profile

from .permissions import IsProfileOwner
from .serializers import (
    ProfileBusinessSerializer,
    ProfileCustomerSerializer,
    ProfileDetailSerializer,
)

User = get_user_model()


class ProfileDetailView(RetrieveUpdateAPIView):
    """View for retrieving and updating a user's profile.
    Only the profile owner can update their profile,
    but any authenticated user can view it.
    """

    queryset = Profile.objects.select_related("user")
    serializer_class = ProfileDetailSerializer
    permission_classes = [IsAuthenticated, IsProfileOwner]


class ProfileBusinessView(ListAPIView):
    """View for listing business profiles.
    Only authenticated users can access this view."""

    serializer_class = ProfileBusinessSerializer

    def get_queryset(self):
        """Return queryset of profiles where the related user's type is 'business'."""
        return Profile.objects.filter(user__type="business")


class ProfileCustomerView(ListAPIView):
    """View for listing customer profiles.
    Only authenticated users can access this view."""

    serializer_class = ProfileCustomerSerializer

    def get_queryset(self):
        return Profile.objects.filter(user__type="customer")
