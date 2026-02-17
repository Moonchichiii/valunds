from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views import View
from passports.selectors import get_passport_data


class PassportDetailView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        try:
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
