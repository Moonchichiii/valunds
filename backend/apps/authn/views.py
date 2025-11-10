from dj_rest_auth.views import LoginView, PasswordResetView


class ThrottledLoginView(LoginView):
    throttle_scope = "login"


class ThrottledPasswordResetView(PasswordResetView):
    throttle_scope = "password_reset"
