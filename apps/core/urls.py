from core.views import DashboardView
from django.http import HttpResponse
from django.urls import path


def healthcheck(_: object) -> HttpResponse:
    return HttpResponse("ok")


urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("health/", healthcheck, name="healthcheck"),
    path("", healthcheck, name="healthcheck"),
]
