import decimal
from typing import Optional

import orjson
from ninja import NinjaAPI
from ninja.renderers import BaseRenderer


def _orjson_default(obj):
    if isinstance(obj, decimal.Decimal):
        return str(obj)


class ORJSONRenderer(BaseRenderer):
    media_type = "application/json"

    def render(self, request, data, *, response_status):
        return orjson.dumps(data, default=_orjson_default)


api = NinjaAPI(title="Factory API", version="v1.0", renderer=ORJSONRenderer())


