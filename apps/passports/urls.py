from django.urls import path
from passports.views import PassportStatusView

app_name = "passports"

urlpatterns = [
    path("me/", PassportStatusView.as_view(), name="detail"),
]
