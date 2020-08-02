from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from domains.serializers import DomainSerializer
from users.serializers import UserSerializer
from .models import User
import jwt
from django.conf import settings


class TokenGetView(APIView):
    def get(self, request):
        try:
            header = request.META.get("HTTP_AUTHORIZATION")
            if header is not None:
                # _, token = header.split(" ")
                token = header
                decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                pk = decoded.get("pk")
                user = User.objects.get(pk=pk)
                return Response(DomainSerializer(user.domains.all(), many=True).data)
        except Exception as e:
            print("error log TokenGetView get : ", e)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                encoded_jwt = jwt.encode(
                    {"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256"
                )
                return Response(data={"token": encoded_jwt})
        except Exception as e:
            print("error log TokenGetView post : ", e)
        return Response(status=status.HTTP_400_BAD_REQUEST)


"""
@api_view(["GET", "POST"])
def save_token(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
        token = json_data["firebase_token"]
        user_os = json_data["user_os"]
        user_ver = json_data["user_ver"]
        print(token)
        try:
            user = models.User.objects.get(token=token)
            if user.domains.count() > 0:
                data = serializers.serialize(
                    "json", user.domains.all(), fields=("url", "title", "change")
                )
                response = HttpResponse(content=data)
                return response
        except models.User.DoesNotExist:
            models.User.objects.create(token=token, user_os=user_os, user_ver=user_ver)
    return Response(status=status.HTTP_200_OK)
"""

