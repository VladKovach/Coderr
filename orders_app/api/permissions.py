from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsCustomerForCreate(BasePermission):
    """Custom permission to only allow customers to create orders."""

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return True

        return request.user.type == "customer"


class IsBusinessOrStaff(BasePermission):
    """Custom permission to only allow staff to delete orders and business users to update orders."""

    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE":
            return request.user.is_staff
        return obj.business_user == request.user
