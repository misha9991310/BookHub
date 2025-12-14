from rest_framework import permissions


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        owner = getattr(obj, "owner", None)

        if owner is None:
            return False

        return owner == request.user
