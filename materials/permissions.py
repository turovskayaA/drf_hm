from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    message = "Вы не являетесь владельцем"

    def has_object_permission(self, request, view, obj):
        is_authenticated = request.user.is_authenticated
        is_owner = obj.owner == request.user
        return is_owner and is_authenticated
