from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsCustomerOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return request.user.type == "customer"


class IsReviewCreator(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.reviewer
