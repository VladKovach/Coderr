from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView

from profiles_app.models import Profile

from .serializers import (
    ProfileBusinessSerializer,
    ProfileCustomerSerializer,
    ProfileDetailSerializer,
)

User = get_user_model()


class ProfileDetailView(RetrieveUpdateAPIView):
    queryset = Profile.objects.select_related("user")
    serializer_class = ProfileDetailSerializer


class ProfileBusinessView(ListAPIView):
    serializer_class = ProfileBusinessSerializer

    def get_queryset(self):
        return Profile.objects.filter(user__type="business")


class ProfileCustomerView(ListAPIView):
    serializer_class = ProfileCustomerSerializer

    def get_queryset(self):
        return Profile.objects.filter(user__type="customer")
