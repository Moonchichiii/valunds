from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.views import View

from valund.passports.selectors import passport_detail


class PassportDetailView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        try:
            passport = passport_detail(str(request.user.id))
        except ObjectDoesNotExist:
            return HttpResponseNotFound("passport-not-found")
        return HttpResponse(f"passport:{passport.id}")
