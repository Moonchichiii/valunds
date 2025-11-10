from django.urls import include, path, reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter


# Central DRF router (register view sets here)
router = DefaultRouter()
# Example later:
# from apps.jobs.views import JobViewSet
# router.register(r"jobs", JobViewSet, basename="jobs")


@api_view(["GET"])
def api_root(request):
    return Response(
        {
            "name": "Valund API",
            "version": "0.1.0",  # docs version, not URL version
            "endpoints": {
                "auth": "/api/auth/",
                "accounts": "/api/accounts/",
                "profiles": "/api/profiles/",
            },
            "schema": request.build_absolute_uri(reverse("schema")),
            "docs": request.build_absolute_uri(reverse("docs")),
        }
    )


urlpatterns = [
    # Optional friendly root
    path("", api_root, name="api-root"),
    # App modules (no /v1)
    path("auth/", include("apps.authn.urls")),  # /api/auth/**
    path("accounts/", include("apps.accounts.urls")),  # /api/accounts/**
    path("profiles/", include("apps.profiles.urls")),  # /api/profiles/**
    # Commented out apps (keep blocked)
    # path("jobs/", include("apps.jobs.urls")),
    # path("applications/", include("apps.applications.urls")),
    # path("matching/", include("apps.matching.urls")),
    # path("cv/", include("apps.cv.urls")),
    # path("contracts/", include("apps.contracts.urls")),
    # path("ratings/", include("apps.ratings.urls")),
    # path("moderation/", include("apps.moderation.urls")),
    # path("scheduling/", include("apps.scheduling.urls")),
    # path("payments/", include("apps.payments.urls")),
    # path("search/", include("apps.search.urls")),
    # Router-registered resources
    path("", include(router.urls)),
]
