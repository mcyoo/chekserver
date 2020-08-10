from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import DomainSerializer
from .models import Domain
from users.models import User
import jwt
from django.conf import settings


class DomainView(APIView):
    def post(self, request):
        try:
            header = request.META.get("HTTP_AUTHORIZATION")
            if header is not None:
                token = header
                decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                pk = decoded.get("pk")
                user = User.objects.get(pk=pk)

                serializer = DomainSerializer(
                    data=request.data, context={"token": user}
                )
                if serializer.is_valid():
                    domain = serializer.save()
                    return Response(status=status.HTTP_200_OK)
                # (ValueError, User.DoesNotExist, Domain.DoesNotExist, IndexError)
        except Exception as e:
            print("error log DomainView post : ", e)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        # print(request.data)
        try:
            index = request.data.get("index")
            # print(index)
            header = request.META.get("HTTP_AUTHORIZATION")
            if header is not None:
                token = header
                decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                pk = decoded.get("pk")
                user = User.objects.get(pk=pk)
                domain = user.domains.all()[index]
                # print(domain)
                domain.delete()
                return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print("error log DomainView put : ", e)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class Toggle_State(APIView):
    def post(self, request):
        try:
            index = request.data.get("index")
            filterling = request.data.get("filterling")

            header = request.META.get("HTTP_AUTHORIZATION")
            if header is not None:
                token = header
                decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                pk = decoded.get("pk")
                user = User.objects.get(pk=pk)
                domain = user.domains.all()[index]

                serializer = DomainSerializer(
                    domain,
                    data=request.data,
                    partial=True,
                    context={"filterling": filterling},
                )
                if serializer.is_valid():
                    domain = serializer.save()
                    return Response(status=status.HTTP_200_OK)

        except Exception as e:
            print("error log Toggle_State put : ", e)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        # print(request.data)
        try:
            index = request.data.get("index")
            # print(index)
            header = request.META.get("HTTP_AUTHORIZATION")
            if header is not None:
                token = header
                decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                pk = decoded.get("pk")
                user = User.objects.get(pk=pk)
                domain = user.domains.all()[index]
                # print(domain)
                domain.change = False
                domain.save()
                return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print("error log Toggle_State put : ", e)
        return Response(status=status.HTTP_400_BAD_REQUEST)


"""
@api_view(["GET", "POST"])
def save_token(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
        token = json_data["firebase_token"]
        user_os = json_data["user_os"]
        user_ver = json_data["user_ver"]
        #print(token)
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

