from rest_framework.permissions import BasePermission, SAFE_METHODS

from reviews.models import User


class IsAdminOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.is_superuser
                     or request.user.role == User.Role.ADMINISTRATOR))


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or (request.user.is_authenticated
                    and (request.user.is_superuser
                         or request.user.role
                         == User.Role.ADMINISTRATOR)))


class IsAdminAuthorModeratorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user.role == User.Role.ADMINISTRATOR
                or request.user.role == User.Role.MODERATOR
                or obj.author == request.user
                )
