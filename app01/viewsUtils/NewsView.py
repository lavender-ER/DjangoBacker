from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from app01 import models
from lxml import etree
from django.http import HttpResponse, JsonResponse, FileResponse
from rest_framework.viewsets import ModelViewSet
import requests
import random
from ..extensions.auth import JwtQueryParamsAuthentication
from ..serializers import NewsModelSerializer
from ..utils import get_token
from .MyPage import MyPag


class NewsViewSet(ModelViewSet):
    parser_classes = [JSONParser, FormParser]
    """视图集"""
    queryset = models.News.objects.all()
    serializer_class = NewsModelSerializer
    pagination_class = MyPag
    # 搜索
    search_fields = ('id', 'title', 'author', 'date')

    @action(methods=['get'], detail=False)
    def topNews(self, request, *args, **kwargs):
        obj = models.News.objects.all().order_by('date')[:5]
        for i in obj:
            i.date = str(i.date)[:10]
        ser = NewsModelSerializer(instance=obj, many=True)
        return JsonResponse({
            'status': 200,
            'msg': '获取数据成功',
            'data': ser.data
        })

    @action(methods=['post'], detail=False)
    def getByDate(self, request, *args, **kwargs):
        start = request.data.get('start', None)
        end = request.data.get('end', None)
        if start and end:
            obj = models.News.objects.filter(date__range=(start, end))
            for i in obj:
                i.date = str(i.date)[:10]
            if obj:
                ser = NewsModelSerializer(instance=obj, many=True)
                print(ser.data)
                return JsonResponse({
                    'code': '200',
                    'msg': '获取数据成功',
                    'data': ser.data
                })
            else:
                return JsonResponse({
                    'code': '1002',
                    'msg': '获取失败',
                })
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False)
    def news(self, request, *args, **kwargs):
        obj = models.News.objects.all().order_by('date')
        for i in obj:
            i.date = str(i.date)[:10]
        ser = NewsModelSerializer(instance=obj, many=True)
        return JsonResponse({
            'status': 200,
            'msg': '获取数据成功',
            'data': ser.data
        })

    # 添加新闻
    @action(methods=['post'], detail=False)
    @csrf_exempt
    def add_news(self, request, *args, **kwargs):
        title = request.data.get('title', None)
        if title:
            obj = models.News.objects.filter(title=title).first()
            if obj:
                return JsonResponse({
                    'status': 202,
                    'msg': '已经存在此新闻名称'
                })
            else:
                serializer = NewsModelSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse({
                        'status': 200,
                        'msg': '添加成功'
                    })
                else:
                    return JsonResponse({
                        'status': 201,
                        'msg': '数据不合法'
                    })
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=False)
    @csrf_exempt
    def get_NewsById(self, request, *args, **kwargs):
        id = request.data.get('id', None)
        if id:
            data = models.News.objects.filter(id=id)
            ser = NewsModelSerializer(instance=data, many=True)
            return JsonResponse({
                'status': 200,
                'msg': '获取数据成功',
                'data': ser.data
            })
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

    # 删除新闻
    @action(methods=['delete'], detail=False)
    @csrf_exempt
    def news_delete(self, request, *args, **kwargs):
        delete_id = request.data.get('id', None)
        if not delete_id:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            obj = models.News.objects.filter(id=delete_id).first()
            if obj:
                obj.delete()
                return JsonResponse({
                    'status': 200,
                    'msg': '删除成功',
                })
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)

    # 修改新闻
    @action(methods=['put'], detail=False)
    @csrf_exempt
    def edit_news(self, request, *args, **kwargs):
        id = request.data.get('id', None)
        if id:
            obj = models.News.objects.get(id=id)
            ser = NewsModelSerializer(instance=obj, data=request.data)
            if ser.is_valid():
                ser.save()
                return JsonResponse({
                    'status': 200,
                    'msg': '更新成功',
                })
            else:
                return JsonResponse({
                    'status': 201,
                    'msg': '修改数据不合法'
                })
        else:
            return Response(status.HTTP_204_NO_CONTENT)
