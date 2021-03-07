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
from ..serializers import BookInfoModelSerializer
from ..utils import get_token
from bs4 import BeautifulSoup
import urllib


class BookViewSet(ModelViewSet):
    parser_classes = [JSONParser, FormParser]
    """视图集"""
    queryset = models.Book.objects.all()
    serializer_class = BookInfoModelSerializer
    # 搜索
    search_fields = ('id', 'name', 'date')

    # 添加推荐书籍
    @action(methods=['post'], detail=False)
    @csrf_exempt
    def add_book(self, request, *args, **kwargs):
        name = request.data.get('name', None)
        if name:
            print(name)
            obj = models.Book.objects.filter(name=name).first()
            if obj:
                return JsonResponse({
                    'status': '201',
                    'msg': '已经存在此书籍名称'
                })
            else:
                serializer = BookInfoModelSerializer(data=request.data)
                print(request.data)
                print(serializer)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse({
                        'status': '200',
                        'msg': '添加成功'
                    })
                else:
                    return JsonResponse({
                        'status': '202',
                        'msg': '插入数据不合法'
                    })
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
        pass

    # 删除书籍
    @action(methods=['delete'], detail=False)
    @csrf_exempt
    def deleteBook(self, request, *args, **kwargs):
        delete_id = request.data.get('id', None)
        if not delete_id:
            return Response(status=status.HTTP_404_NOT_FOUND)
        obj = models.Book.objects.filter(id=delete_id).first()
        if obj:
            obj.delete()
            return JsonResponse({
                'status': 200,
                'msg': '删除成功',
            })
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False)
    def getAll(self, request, *args, **kwargs):
        obj = models.Book.objects.all().order_by('date')
        if obj:
            ser = BookInfoModelSerializer(instance=obj, many=True)
            return JsonResponse({
                'status': 200,
                'msg': '获取数据成功',
                'data': ser.data
            })
        else:
            return JsonResponse({
                'status': 201,
                'msg': '获取失败',
            })

    # # 获取单个书籍信息
    # @action(methods=['get'], detail=False)
    # @csrf_exempt
    # def single_book(self, request, *args, **kwargs):
    #     query_name = request.data.get('name', None)
    #     print(query_name)
    #     if not query_name:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #     else:
    #         href = models.Book.objects.all().filter(name=query_name)
    #         serializer = BookInfoModelSerializer(instance=href, many=True)
    #         print(serializer.data)
    #         return JsonResponse({
    #             'code': 2010,
    #             'msg': '查询成功',
    #             'data': serializer.data
    #         })

    # 修改信息
    @action(methods=['put'], detail=False)
    @csrf_exempt
    def edit_book(self, request, *args, **kwargs):
        name = request.data.get('name', None)
        if name:
            obj = models.Book.objects.filter(name=name).first()
            serializer = BookInfoModelSerializer(instance=obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(update_fields=['name', 'publisher'])
                return JsonResponse({
                    'status': 200,
                    'msg': '更新成功',
                })
            else:
                return JsonResponse({
                    'status': 201,
                    'msg': '更新失败',
                })
        else:
            return Response(status.HTTP_204_NO_CONTENT)
