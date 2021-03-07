from __future__ import unicode_literals
import os
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from app01 import models
from django.http import HttpResponse, JsonResponse, FileResponse
from rest_framework.viewsets import ModelViewSet
from djangoTest import settings
from ..extensions.auth import JwtQueryParamsAuthentication
from ..serializers import UserModelSerializer
from ..utils import get_token


class UserViewSet(ModelViewSet):
    parser_classes = [MultiPartParser, JSONParser, FormParser]
    """视图集"""
    queryset = models.User.objects.all()
    serializer_class = UserModelSerializer
    # 搜索
    search_fields = ('id')
    secret_id = settings.cos_secret_id  # 替换为用户的 secretId
    secret_key = settings.cos_secret_key  # 替换为用户的 secretKey
    region = 'ap-nanjing'  # 替换为用户的 Region
    token = None  # 使用临时密钥需要传入 Token，默认为空，可不填
    scheme = 'http'  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
    baseurl = 'https://user-1254029770.cos.ap-nanjing.myqcloud.com/'
    Bucket = 'user-1254029770'

    def loginCos(self):
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        config = CosConfig(Region=self.region, SecretId=self.secret_id, SecretKey=self.secret_key, Token=self.token,
                           Scheme=self.scheme)
        client = CosS3Client(config)
        return client

    # 添加资源
    @action(methods=['post'], detail=False)
    @csrf_exempt
    def add_user(self, request, *args, **kwargs):
        name = request.data.get('name', None)
        if name:
            print(name)
            obj = models.User.objects.filter(name=name).first()
            if obj:
                return JsonResponse({
                    'status': 202,
                    'msg': '已经存在此用户名称'
                })
            else:
                serializer = UserModelSerializer(data=request.data)

                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse({
                        'status': 200,
                        'msg': '添加成功'
                    })
                else:
                    return JsonResponse({
                        'status': 201,
                        'msg': '插入数据不合法'
                    })
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=False)
    @csrf_exempt
    def update_Info(self, request, *args, **kwargs):
        file = request.FILES.get("file", None)
        id = request.data.get('id', None)
        name = request.data.get('name', None)
        uid = request.data.get('uid', None)
        type = request.data.get('type', None)
        note = request.data.get('note', None)

        if file and id:
            obj = models.User.objects.filter(id=id).first()
            if obj:
                print(obj.uid)
                filetype = os.path.splitext(str(file))[1]
                filename = uid + filetype
                client = self.loginCos()

                if obj.uid != '':
                    print(obj.uid)
                    response = client.delete_object(
                        Bucket=self.Bucket,
                        Key=obj.uid
                    )
                response = client.put_object(
                    Bucket=self.Bucket,
                    Body=file,
                    Key=filename,
                    ContentType=type,
                    StorageClass='STANDARD',
                    EnableMD5=False
                )
                if (response['ETag']):
                    fileUrl = self.baseurl + filename
                    obj.uid = fileUrl
                    obj.filename = uid + filetype
                    obj.name = name
                    obj.note = note
                    obj.save()
                    return JsonResponse({
                        'status': 200,
                        'msg': '上传成功'
                    })
                else:
                    return JsonResponse({
                        'status': 202,
                        'msg': '上传失败'
                    })
            else:
                return JsonResponse({
                    'status': 201,
                    'msg': '更新失败'
                })
        else:
            obj = models.User.objects.filter(id=id).first()
            if obj:
                obj.name = name
                obj.note = note
                obj.save()
                return JsonResponse({
                    'status': 200,
                    'msg': '上传成功'
                })
            return Response(status=status.HTTP_204_NO_CONTENT)

    # 获取所有info
    @action(methods=['post'], detail=False)
    @csrf_exempt
    def get_InfoById(self, request, *args, **kwargs):
        id = request.data.get('id', None)
        if id:
            data = models.User.objects.filter(id=id)
            ser = UserModelSerializer(instance=data, many=True)
            return JsonResponse({
                'status': 200,
                'msg': '获取数据成功',
                'data': ser.data
            })
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
