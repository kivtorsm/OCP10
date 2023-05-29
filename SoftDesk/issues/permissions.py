from django.db.models import Q

from rest_framework import permissions
from rest_framework.generics import get_object_or_404

from issues.models import Contributor, Project

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it
    """

    def has_object_permission(self, request, view, obj):

        # Read permissions are allowed to authenticated users contributing to a project
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object
        if isinstance(obj, Project):
            owner = get_object_or_404(
                Contributor.objects.filter(
                    Q(project_id=obj) & Q(permission='AUTHOR')
                )
            )
            return request.user == owner.user_id
        else:
            return request.user == obj.author_user_id
