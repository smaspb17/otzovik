from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsModerator(BasePermission):
    pass


class IsAdmin(BasePermission):
    pass


class IsAuthorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user
