import jwt
import datetime
from django.conf import settings


def get_token(payload, timeout):
    salt = settings.SECRET_KEY
    headers = {
        "typ": "jwt_",
        "alg": "HS256",
    }
    payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(minutes=timeout)  # 设置到期时间
    token = jwt.encode(payload=payload, key=salt, headers=headers).decode("utf-8")
    return token
