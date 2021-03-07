from __future__ import unicode_literals
from django.http import HttpResponse, JsonResponse, FileResponse
from rest_framework.viewsets import ModelViewSet
from ..serializers import UserModelSerializer
from ..utils import get_token
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from app01 import models


class LoginViewSet(ModelViewSet):
    parser_classes = [MultiPartParser, JSONParser, FormParser]
    # authentication_classes = []
    """视图集"""
    queryset = models.User.objects.all()
    serializer_class = UserModelSerializer
    # 搜索
    search_fields = ('id')

    @action(methods=['post'], detail=False)
    @csrf_exempt
    def LogOn(self, request, *args, **kwargs):
        print(request.body)
        username = request.data.get("username")
        pwd = request.data.get("password")
        # print(username)
        # print(pwd)
        user_obj = models.User.objects.filter(nickname=username, pwd=pwd).first()
        if not user_obj:
            return Response({"code": 1000, 'error': '用户名或密码错误'})
        payload = {
            "id": user_obj.pk,
            "name": user_obj.nickname,
        }
        token = get_token(payload, 1)
        print(token)
        return Response({"status": 200, 'data': token, 'id': user_obj.pk})

    @action(methods=['post'], detail=False)
    @csrf_exempt
    def register(self, request, *args, **kwargs):
        # username = request.query_params.get('nickname')
        username = request.data.get("nickname")
        pwd = request.data.get("pwd")
        print(username)
        if username and pwd:
            models.User.objects.create(nickname=username, pwd=pwd)
            # serializer = UserModelSerializer(data=request.data)
            # print(serializer.is_valid(raise_exception=True))
            # if serializer.is_valid(raise_exception=True):
            #     serializer.save()
            user_obj = models.User.objects.filter(nickname=username, pwd=pwd).first()
            print(user_obj)
            payload = {
                "id": user_obj.id,
                "name": user_obj.nickname,
            }
            token = get_token(payload, 1)
            return JsonResponse({
                'status': 200,
                'msg': '添加成功',
                'data': token,
                'id': user_obj.id
            })
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
