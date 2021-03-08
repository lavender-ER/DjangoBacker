from __future__ import unicode_literals
import os
from datetime import datetime
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
from ..serializers import SourceModelSerializer


class ResourceViewSet(ModelViewSet):
    parser_classes = [MultiPartParser, JSONParser, FormParser]
    """视图集"""
    queryset = models.Source.objects.all()
    serializer_class = SourceModelSerializer
    # 搜索
    search_fields = ('id')
    secret_id = settings.cos_secret_id  # 替换为用户的 secretId
    secret_key = settings.cos_secret_key  # 替换为用户的 secretKey
    region = 'ap-guangzhou'  # 替换为用户的 Region
    token = None  # 使用临时密钥需要传入 Token，默认为空，可不填
    scheme = 'http'  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
    Bucket = 'costest-1254029770'
    baseurl = 'https://costest-1254029770.cos.ap-guangzhou.myqcloud.com/'

    def loginCos(self):
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        config = CosConfig(Region=self.region, SecretId=self.secret_id, SecretKey=self.secret_key, Token=self.token,
                           Scheme=self.scheme)
        client = CosS3Client(config)
        return client

    @action(methods=['get'], detail=False)
    @csrf_exempt
    def get_resourceInfo(self, request, *args, **kwargs):
        obj = models.Source.objects.all().order_by('date')
        ser = SourceModelSerializer(instance=obj, many=True)
        return JsonResponse({
            'status': 200,
            'msg': '获取数据成功',
            'data': ser.data
        })

    @action(methods=['post'], detail=False)
    @csrf_exempt
    def add_resource(self, request, *args, **kwargs):
        file = request.FILES.get("file", None)
        desc = request.data.get('desc', None)
        name = request.data.get('name', None)
        uid = request.data.get('uid', None)
        type = request.data.get('type', None)
        size = request.data.get('size', None)
        uploader = request.data.get('uploader', None)

        if file and desc and name and uid and type and size and uploader:
            filetype = os.path.splitext(str(file))[1]
            filename = uid + filetype
            client = self.loginCos()
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
                models.Source.objects.create(uploader=uploader, memory=size, name=name + filetype,
                                             desc=desc, date=datetime.now(), file=fileUrl, uid=filename)
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
                'msg': '所需信息缺失'
            })

    # 删除资源
    @action(methods=['delete'], detail=False)
    @csrf_exempt
    def deleteSource(self, request, *args, **kwargs):
        delete_id = request.data.get('id', None)
        if not delete_id:
            return Response(status=status.HTTP_404_NOT_FOUND)
        obj = models.Source.objects.filter(id=delete_id).first()
        client = self.loginCos()
        response = client.delete_object(
            Bucket=self.Bucket,
            Key=obj.uid
        )
        obj.delete()
        return JsonResponse({
            'status': 200,
            'msg': '删除成功',
        })

    # 修改资源
    @action(methods=['put'], detail=False)
    @csrf_exempt
    def edit_resource(self, request, *args, **kwargs):
        id = request.data.get('id', None)
        desc = request.data.get('desc', None)
        name = request.data.get('name', None)
        if id and desc and desc:
            try:
                obj = models.Source.objects.get(id=id)
                obj.desc = desc
                obj.name = name
                obj.save()
                return JsonResponse({
                    'status': 200,
                    'msg': '更新成功',
                })
            except:
                return JsonResponse({
                    'status': 201,
                    'msg': '更新失败',
                })
        else:
            return Response(status.HTTP_204_NO_CONTENT)
