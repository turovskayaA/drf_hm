from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    massage = "Вы не являетесь владельцем"

    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        return False
