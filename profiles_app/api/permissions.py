from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsProfileOwner(BasePermission):
    """Object-level permission for Profile detail operations.
    GET : allowed

    PATCH/PUT: Profile owner
    """

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True
        elif request.method == "PATCH" or request.method == "PUT":
            return obj.user == request.user
