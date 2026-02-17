from django.urls import path
from passports.views import PassportDetailView

app_name = "passports"

urlpatterns = [
    path("me/", PassportDetailView.as_view(), name="detail"),
]
