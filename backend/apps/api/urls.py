from django.urls import include, path
from rest_framework.routers import DefaultRouter


# Central DRF router (register viewsets here as they appear)
router = DefaultRouter()
# Example later:
# from apps.jobs.views import JobViewSet
# router.register(r"jobs", JobViewSet, basename="jobs")

urlpatterns = [
    path(
        "v1/",
        include(
            [
                path("auth/", include("apps.authn.urls")),
                path("accounts/", include("apps.accounts.urls")),
                path("profiles/", include("apps.profiles.urls")),
                path("jobs/", include("apps.jobs.urls")),
                path("applications/", include("apps.applications.urls")),
                path("matching/", include("apps.matching.urls")),
                path("cv/", include("apps.cv.urls")),
                path("contracts/", include("apps.contracts.urls")),
                path("ratings/", include("apps.ratings.urls")),
                path("moderation/", include("apps.moderation.urls")),
                path("scheduling/", include("apps.scheduling.urls")),
                path("payments/", include("apps.payments.urls")),
                path("search/", include("apps.search.urls")),
            ]
        ),
    ),
    path("", include(router.urls)),
]
