from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "phone",
            "address_line1",
            "address_line2",
            "postal_code",
            "city",
            "region",
            "country",
            "language",
            "marketing_opt_in",
        ]
