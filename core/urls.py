from django.urls import path
from . import views

app_name = "core"
# room_views.all_rooms 함수 실행함
urlpatterns = [
    path("home/", views.home, name="home"),
    path("userservice/", views.userservice, name="userservice"),
]
