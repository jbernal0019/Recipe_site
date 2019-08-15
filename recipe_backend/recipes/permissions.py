
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to modify/edit it.
    Read only is allowed to other users.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the authenticated user.
        return request.user.is_authenticated and (obj.owner == request.user)


class IsRecipeOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow the owner of a recipe associated to an object
    to modify/edit it. Read only is allowed to other users.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the related recipe.
        return request.user.is_authenticated and (obj.recipe.owner == request.user)
