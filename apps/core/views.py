from __future__ import annotations

from typing import TYPE_CHECKING

from django.shortcuts import render
from django.views import View

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


class BaseHtmxView(View):
    """Serve full pages or HTMX fragments from a single orchestration point."""

    template_name = ""
    partial_template_name = ""

    def get_context_data(
        self,
        request: HttpRequest,
        **kwargs: object,
    ) -> dict[str, object]:
        return {"request": request, **kwargs}

    def get(self, request: HttpRequest, **kwargs: object) -> HttpResponse:
        context = self.get_context_data(request, **kwargs)
        if request.headers.get("HX-Request") == "true" and self.partial_template_name:
            return render(request, self.partial_template_name, context)
        return render(request, self.template_name, context)


class DashboardView(BaseHtmxView):
    template_name = "pages/dashboard.html"
