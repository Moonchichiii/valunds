from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

from .social import GithubLogin, GoogleLogin
from .views import ThrottledLoginView, ThrottledPasswordResetView


urlpatterns = [
    path("login/", ThrottledLoginView.as_view(), name="login"),
    path("password/reset/", ThrottledPasswordResetView.as_view(), name="rest_password_reset"),
    path("", include("dj_rest_auth.urls")),
    path("registration/", include("dj_rest_auth.registration.urls")),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("social/google/", GoogleLogin.as_view(), name="google_login"),
    path("social/github/", GithubLogin.as_view(), name="github_login"),
]
