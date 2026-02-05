from rest_framework.permissions import BasePermission


class IsProfileOwner(BasePermission):
    """Object-level permission for Profile detail operations.


    PATCH/PUT: Profile owner
    """

    def has_object_permission(self, request, view, obj):
        if request.method == "PATCH" or request.method == "PUT":
            print("obj.user = ", obj.user)
            print("request.user = ", request.user)
            return obj.user == request.user
