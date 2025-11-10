from django.urls import path

from .views import MeUpdateView, MeView


app_name = "accounts"

urlpatterns = [
    path("me/", MeView.as_view(), name="me"),
    path("me/update/", MeUpdateView.as_view(), name="me_update"),
]
