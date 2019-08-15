
from rest_framework import permissions


class IsUser(permissions.BasePermission):
    """
    Custom permission to only allow access to the authenticated user.
    """

    def has_object_permission(self, request, view, obj):
        # permissions are only allowed to the authenticated user.
        return obj == request.user
