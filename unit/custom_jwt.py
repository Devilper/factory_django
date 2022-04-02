import jwt
from django.contrib.auth.backends import ModelBackend
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication
from rest_framework_jwt.utils import jwt_decode_handler

from user.models import UserProfile


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(username=username)
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class JwtAuthentication(BaseJSONWebTokenAuthentication):
    """
    当User表为自定义的表，而且没有继承自django自带的auth.User表时，需要重写验证方法：authenticate
    """
    def authenticate(self, request):
        token = request.META.get('HTTP_Authorization'.upper())
        print(token)
        try:
            payload = jwt_decode_handler(token)
        except jwt.ExpiredSignature:
            raise AuthenticationFailed('亲，token放太久了，都过期了，快去重新获取吧！')
        except jwt.DecodeError:
            raise AuthenticationFailed('token为空或者解码错误')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('不合法的token')
        # 得到的user对象，应该是自己user表的user对象
        # print(payload)
        # payload内容:{'user_id': 1, 'username': '66559575', 'exp': 1620538525, 'email': '66559575@cho.cn'}
        user = UserProfile.objects.get(id=payload['user_id'])
        # user = payload
        return user, token

