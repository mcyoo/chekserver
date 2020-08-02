from rest_framework import authentication
from users.models import User


class TokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        try:
            header = request.META.get("HTTP_AUTHORIZATION")
            if header is None:
                return None
            _, token = header.split(" ")
            user = User.objects.get(token=token)
            return (user, None)
        except (ValueError, User.DoesNotExist):
            return None
