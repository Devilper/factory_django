import decimal
from typing import Optional

import orjson
from django.http import JsonResponse
from ninja import NinjaAPI
from ninja.errors import ValidationError, HttpError
from ninja.renderers import BaseRenderer


def _orjson_default(obj):
    if isinstance(obj, decimal.Decimal):
        return str(obj)


class ORJSONRenderer(BaseRenderer):
    media_type = "application/json"

    def render(self, request, data, *, response_status):
        return orjson.dumps(data, default=_orjson_default)


api = NinjaAPI(title="Factory API", version="v1.0", renderer=ORJSONRenderer())


# @api.exception_handler(ValidationError)
# def validation_errors(request, exc: ValidationError):
#     print("ssdsadadasdsdsdsds")
#     print(exc)
#     return JsonResponse({
#         "code": "500",
#         "desc": f"{exc}"
#     })
#
#
# @api.exception_handler(HttpError)
# def validation_errors(request, exc: HttpError):
#     print("sssssssssssss")
#     print(exc)
#     return JsonResponse({
#         "code": "500",
#         "desc": f"{exc}"
#     },
#     status=400)