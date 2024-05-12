from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        is_authenticated = user.is_authenticated
        is_moderator = user.groups.filter(name='moderator').exists()
        return is_authenticated and is_moderator
