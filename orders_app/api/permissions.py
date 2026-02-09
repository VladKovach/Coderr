from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsCustomerForCreate(BasePermission):

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return True

        return request.user.type == "customer"


class IsBusinessOrStaff(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE":
            return request.user.is_staff
        return request.user.type == "business"
