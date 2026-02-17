from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views import View
from passports.selectors import get_passport_context
from passports.selectors import get_passport_data
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.views import View
from passports.selectors import passport_detail


class PassportDetailView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        try:
            payload = get_passport_context(str(request.user.id))
            payload = get_passport_data(str(request.user.id))
        except ObjectDoesNotExist:
            return HttpResponse("passport-not-found", status=404)

        if request.headers.get("HX-Request") == "true":
            return HttpResponse(
                "passport:{id}:{sector}".format(
                    id=payload["id"],
                    sector=payload["sector"],
                )
            )
        return JsonResponse(payload)
            passport_id = payload["id"]
            verification_tier = payload["verification_tier"]
            return HttpResponse(f"passport:{passport_id}:{verification_tier}")
        return JsonResponse(payload)
            passport = passport_detail(str(request.user.id))
        except ObjectDoesNotExist:
            return HttpResponseNotFound("passport-not-found")
        return HttpResponse(f"passport:{passport.id}")
