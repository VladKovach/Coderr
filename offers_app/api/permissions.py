from django.contrib.auth import get_user_model
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsBusinessUser(BasePermission):
    """permission for Offer operations.
    POST: type business only"""

    def has_permission(self, request, view):
        return request.user.type == "business"


class IsOfferOwner(BasePermission):
    """Object-level permission for Offer Detail operations.
    PATCH: owner  only"""

    def has_object_permission(self, request, view, obj):

        return obj.user == request.user
