from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it
    """

    def has_object_permission(self, request, view, obj):

        # Read permissions are allowed to authenticated users contributing to a project
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the oject
        return request.user == obj.user_id | request.user == obj.author_user_id
