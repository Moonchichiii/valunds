from django.urls import path

from .views import MyProfileView


app_name = "profiles"

urlpatterns = [
    path("me/", MyProfileView.as_view(), name="my_profile"),
]
