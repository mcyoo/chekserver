from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("token/", views.TokenGetView.as_view(), name="token"),
]
