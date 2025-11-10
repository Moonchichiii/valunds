# apps/authn/urls.py
from allauth.account.views import confirm_email
from django.urls import include, path, re_path
from rest_framework_simplejwt.views import TokenRefreshView

from .social import GithubLogin, GoogleLogin
from .views import ThrottledLoginView, ThrottledPasswordResetView


urlpatterns = [
    # Email confirmation (override the dj-rest-auth placeholder)
    re_path(
        r"^registration/account-confirm-email/(?P<key>[-:\w]+)/$",
        confirm_email,
        name="account_confirm_email",
    ),
    # Auth endpoints (mount throttled ones explicitly)
    path("login/", ThrottledLoginView.as_view(), name="login"),
    path("password/reset/", ThrottledPasswordResetView.as_view(), name="rest_password_reset"),
    # dj-rest-auth default routes (logout, password-change, verify-email, etc.)
    path("", include("dj_rest_auth.urls")),
    path("registration/", include("dj_rest_auth.registration.urls")),
    # JWT refresh + social
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("social/google/", GoogleLogin.as_view(), name="google_login"),
    path("social/github/", GithubLogin.as_view(), name="github_login"),
]
