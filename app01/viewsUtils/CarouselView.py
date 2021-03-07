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
from ..serializers import CarouselModelSerializer
from djangoTest import settings


class CarouselViewSet(ModelViewSet):
    parser_classes = [MultiPartParser, JSONParser, FormParser]
    """视图集"""
    queryset = models.Carousel.objects.all()
    serializer_class = CarouselModelSerializer
    # 搜索
    search_fields = ('id', 'image')
    secret_id = settings.cos_secret_id  # 替换为用户的 secretId
    secret_key = settings.cos_secret_key  # 替换为用户的 secretKey
    region = 'ap-nanjing'  # 替换为用户的 Region
    token = None  # 使用临时密钥需要传入 Token，默认为空，可不填
    scheme = 'http'  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
    Bucket = 'carousel-1254029770'
    baseurl = 'https://carousel-1254029770.cos.ap-nanjing.myqcloud.com/'

    def loginCos(self):
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        config = CosConfig(Region=self.region, SecretId=self.secret_id, SecretKey=self.secret_key, Token=self.token,
                           Scheme=self.scheme)
        client = CosS3Client(config)
        return client

    # 添加轮播图
    @action(methods=['post'], detail=False)
    @csrf_exempt
    def add_carousel(self, request, *args, **kwargs):
        file = request.FILES.get('file', None)
        uid = request.data.get('uid', None)
        typefile = request.data.get('type', None)
        if file and uid and typefile:
            filetype = os.path.splitext(str(file))[1]
            filename = uid + filetype
            client = self.loginCos()
            response = client.put_object(
                Bucket=self.Bucket,
                Body=file,
                Key=filename,
                ContentType=typefile,
                StorageClass='STANDARD',
                EnableMD5=False
            )
            # print(response['ETag'])
            if (response['ETag']):
                fileUrl = self.baseurl + filename
                models.Carousel.objects.create(image=fileUrl, filename=filename)
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

    # 删除轮播图
    @action(methods=['delete'], detail=False)
    @csrf_exempt
    def deleteCar(self, request, *args, **kwargs):
        delete_id = request.data.get('id', None)
        if not delete_id:
            return Response(status=status.HTTP_404_NOT_FOUND)
        obj = models.Carousel.objects.filter(id=delete_id).first()
        if obj:
            client = self.loginCos()
            print(obj.filename)
            response = client.delete_object(
                Bucket=self.Bucket,
                Key=obj.filename
            )
            obj.delete()
            return JsonResponse({
                'status': 200,
                'msg': '删除成功',
            })
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False)
    @csrf_exempt
    def get_carouselInfo(self, request, *args, **kwargs):
        obj = models.Carousel.objects.all()
        ser = CarouselModelSerializer(instance=obj, many=True)
        return JsonResponse({
            'status': 200,
            'msg': '获取数据成功',
            'data': ser.data
        })
