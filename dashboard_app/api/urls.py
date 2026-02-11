from django.urls import path

from dashboard_app.api.views import base_info_view

urlpatterns = [path("base-info/", base_info_view, name="baseinfo")]
