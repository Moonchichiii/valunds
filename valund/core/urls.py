from django.http import HttpResponse
from django.urls import path


def healthcheck(_: object) -> HttpResponse:
    return HttpResponse("ok")


urlpatterns = [
    path("", healthcheck, name="healthcheck"),
]
