from django.urls import path
from profiles.views import ProfileIdentityCardView

app_name = "profiles"

urlpatterns = [
    path("me/identity-card/", ProfileIdentityCardView.as_view(), name="identity-card"),
]
