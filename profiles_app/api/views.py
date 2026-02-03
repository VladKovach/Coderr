from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveUpdateAPIView

from profiles_app.models import Profile

from .serializers import ProfileDetailSerializer

User = get_user_model()


class ProfileDetailView(RetrieveUpdateAPIView):
    queryset = Profile.objects.select_related("user")
    serializer_class = ProfileDetailSerializer
