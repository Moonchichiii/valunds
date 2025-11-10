from rest_framework import permissions
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.request import Request
from rest_framework.throttling import ScopedRateThrottle

from apps.accounts.serializers import UserSerializer


class MeThrottle(ScopedRateThrottle):
    scope = "me"


class MeView(RetrieveAPIView):
    """Retrieve authenticated user. Call once on app bootstrap."""

    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [MeThrottle]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def retrieve(self, request: Request, *args, **kwargs):
        # Encourage client caching for a short window; your frontend plan already
        # disables aggressive refetching — this just adds server-side hints.
        response = super().retrieve(request, *args, **kwargs)
        response["Cache-Control"] = "private, max-age=60"
        return response


class MeUpdateView(UpdateAPIView):
    """Update user profile basics (first_name/last_name only)."""

    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [MeThrottle]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
