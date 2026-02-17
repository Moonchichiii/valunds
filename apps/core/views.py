from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import View


class AsyncHTMXView(View):
    """Base async view optimized for HTMX fragment responses."""

    template_name = ""
    fragment_template_name = ""

    async def get(
        self,
        request: HttpRequest,
        *_: object,
        **kwargs: object,
    ) -> HttpResponse:
        context = await self.get_context_data(request=request, **kwargs)
        if request.headers.get("HX-Request") == "true" and self.fragment_template_name:
            return render(request, self.fragment_template_name, context)
        return render(request, self.template_name, context)

    async def get_context_data(
        self,
        *,
        request: HttpRequest,
        **kwargs: object,
    ) -> dict[str, object]:
        return {"request": request, **kwargs}
