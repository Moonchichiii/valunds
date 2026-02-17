from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string
from django.views import View
from profiles.selectors import profile_get_searchable_base


class ProfileIdentityCardView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        profile = profile_get_searchable_base().filter(user=request.user).first()
        if profile is None:
            return HttpResponse("profile-not-found", status=404)
        html = render_to_string(
            "profiles/components/identity_card.html",
            {"profile": profile},
            request=request,
        )
        return HttpResponse(html)
