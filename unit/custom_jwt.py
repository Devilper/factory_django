from datetime import datetime, timedelta

import jwt

from factory_django.settings import JWT_SECRET_KEY


def get_jwt_token(username, staff_code, u_id):
    """
    生成jwt-token
    :param username:
    :param staff_code:
    :param u_id:
    :return:
    """
    payload = {
        'exp': datetime.utcnow() + timedelta(days=1),  # 单位秒
        'iat': datetime.utcnow(),
        'data': {'username': username, 'staff_code': staff_code, 'id':u_id}
    }
    encoded_jwt = jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')
    return encoded_jwt


def decode_jwt_token(encoded_jwt):
    # 关闭过期时间检验
    de_code = jwt.decode(encoded_jwt, JWT_SECRET_KEY, algorithms=['HS256'])
    return de_code


def decode_jwt(token):
    try:
        token_info = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])['data']
    except Exception as e:
        return None
    return token_info
