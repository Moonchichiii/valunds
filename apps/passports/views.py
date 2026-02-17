from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from passports.selectors import get_passport_data


class PassportStatusView(View):
    def get(
        self,
        request: HttpRequest,
        *args: object,
        **kwargs: object,
    ) -> HttpResponse:
        _ = (args, kwargs)
        if not request.user.is_authenticated:
            return HttpResponse(status=401)
        data = get_passport_data(request.user.id)
        return JsonResponse(data)


class PassportCredentialBadgeView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        if not request.user.is_authenticated:
            return HttpResponse(status=401)
        data = get_passport_data(request.user.id)
        status = "VERIFIED" if data["verified"] else "PENDING"
        return render(
            request,
            "passports/components/credential_badge.html",
            {
                "credential": {
                    "status": status,
                }
            },
        )
