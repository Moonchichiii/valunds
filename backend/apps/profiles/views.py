from rest_framework import permissions
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.throttling import ScopedRateThrottle

from .models import Profile
from .serializers import ProfileSerializer


class ProfileThrottle(ScopedRateThrottle):
    scope = "profile"


class MyProfileView(RetrieveUpdateAPIView):
    """Retrieve/update authenticated user's encrypted profile."""

    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [ProfileThrottle]
    serializer_class = ProfileSerializer

    def get_object(self):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile
