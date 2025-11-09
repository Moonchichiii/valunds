from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

from .social import GithubLogin, GoogleLogin


urlpatterns = [
    path("", include("dj_rest_auth.urls")),  # /login/ /logout/ /password/
    path("registration/", include("dj_rest_auth.registration.urls")),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Social login (token exchange → returns your JWT)
    path("social/google/", GoogleLogin.as_view(), name="google_login"),
    path("social/github/", GithubLogin.as_view(), name="github_login"),
]
