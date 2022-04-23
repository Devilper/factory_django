from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from restapi.base import ORJSONRenderer
from restapi.schema import ApiError, ApiResponse
from unit.custom_jwt import decode_jwt


WHITE_LIST = [
    '/api/login/',
    '/admin/'
]


class RequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        if path not in WHITE_LIST:
            token = request.META.get("HTTP_AUTHORIZATION")
            if token:
                user_info = decode_jwt(token)
                print(f"user_info:{user_info}")
                setattr(request, "user", user_info)
            else:
                return JsonResponse(data={"code": 500, "msg": "请重新登录"})
        response = self.get_response(request)
        return response


