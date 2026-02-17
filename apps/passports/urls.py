from django.urls import path
from passports.views import PassportCredentialBadgeView, PassportStatusView
from passports.views import PassportStatusView
from passports.views import PassportDetailView

app_name = "passports"

urlpatterns = [
    path("me/", PassportStatusView.as_view(), name="detail"),
    path("me/badge/", PassportCredentialBadgeView.as_view(), name="badge"),
    path("me/", PassportDetailView.as_view(), name="detail"),
]
