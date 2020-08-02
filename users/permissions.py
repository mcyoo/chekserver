from rest_framework.permissions import BasePermission
from users.models import User


class IsSelf(BasePermission):
    def has_permission(self, request, view):
        try:
            header = request.META.get("HTTP_AUTHORIZATION")
            if header is None:
                return False
            _, token = header.split(" ")
            User.objects.get(token=token)
            return True
        except (ValueError, User.DoesNotExist):
            pass
        return False
