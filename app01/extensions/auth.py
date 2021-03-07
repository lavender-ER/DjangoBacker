import jwt
from jwt import exceptions
from rest_framework.authentication import BaseAuthentication
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed


class JwtQueryParamsAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.query_params.get("token")
        salt = settings.SECRET_KEY
        try:
            result = jwt.decode(token, salt, True)
        except exceptions.ExpiredSignatureError:
            msg = "token失效"
            raise AuthenticationFailed({"code": 1001, "msg": msg})
        except exceptions.DecodeError:
            msg = "token认证失败"
            raise AuthenticationFailed({"code": 1002, "msg": msg})

        except exceptions.InvalidTokenError:
            msg = "非法token"
            raise AuthenticationFailed({"code": 1003, "msg": msg})

        return (result, token)

        # 三种操作
        # 1.抛出错误，后续不再执行
        # 2.return一个元组，（1,2）认证通过，在视图中如果调用request.user 就是第一个值request.auth就是第二个
        # 3.None不做任何操作
