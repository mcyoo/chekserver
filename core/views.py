from django.shortcuts import render


def home(request):
    return render(request, "index.html")


def userservice(request):
    return render(request, "chekapp.html")
