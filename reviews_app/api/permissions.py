from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsCustomerOrReadOnly(BasePermission):
    """Allow read-only access to everyone, but only allow customers to create or modify reviews."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return request.user.type == "customer"


class IsReviewCreator(BasePermission):
    """Allow only the creator of the review to modify or delete it."""

    def has_object_permission(self, request, view, obj):
        return request.user == obj.reviewer
