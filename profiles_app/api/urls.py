from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from profiles_app.api.views import (
    ProfileBusinessView,
    ProfileCustomerView,
    ProfileDetailView,
)

urlpatterns = [
    path(
        "profile/<int:pk>/",
        ProfileDetailView.as_view(),
        name="profile-detail",
    ),
    path(
        "profiles/business/",
        ProfileBusinessView.as_view(),
        name="profile-detail",
    ),
    path(
        "profiles/customer/",
        ProfileCustomerView.as_view(),
        name="profile-detail",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
