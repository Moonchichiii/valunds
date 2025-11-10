from rest_framework.views import exception_handler as drf_handler


def problem_exception_handler(exc, context):
    resp = drf_handler(exc, context)
    if not resp:
        return resp
    resp["Content-Type"] = "application/problem+json"
    return resp
