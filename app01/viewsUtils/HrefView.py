from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from app01 import models
from django.http import HttpResponse, JsonResponse, FileResponse
from rest_framework.viewsets import ModelViewSet
from ..extensions.auth import JwtQueryParamsAuthentication
from ..serializers import HrefInfoModelSerializer
from .MyPage import MyPag


class HrefViewSet(ModelViewSet):
    parser_classes = [JSONParser, FormParser]
    """视图集"""
    queryset = models.Href.objects.all()
    serializer_class = HrefInfoModelSerializer
    ordering = ('id')
    pagination_class = MyPag
    # 搜索
    search_fields = ('id', 'name')

    @action(methods=['get'], detail=False)
    def hrefs(self, request, *args, **kwargs):
        obj = models.Href.objects.all()
        if obj:
            ser = HrefInfoModelSerializer(instance=obj, many=True)
            return JsonResponse({
                'status': 200,
                'msg': '获取数据成功',
                'data': ser.data
            })
        else:
            return JsonResponse({
                'status': '201',
                'msg': '获取失败',
            })

    # 添加链接
    @action(methods=['post'], detail=False)
    @csrf_exempt
    def add_href(self, request, *args, **kwargs):
        name = request.data.get('name', None)
        if name:
            print(name)
            obj = models.Href.objects.filter(name=name).first()
            if obj:
                return JsonResponse({
                    'status': 201,
                    'msg': '已经存在此链接名称'
                })
            else:
                serializer = HrefInfoModelSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse({
                        'status': 200,
                        'msg': '添加成功'
                    })
                else:
                    return JsonResponse({
                        'status': 202,
                        'msg': '插入数据不合法'
                    })
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
        pass

    # 删除链接
    @action(methods=['delete'], detail=False)
    @csrf_exempt
    def deleteLink(self, request, *args, **kwargs):
        delete_id = request.data.get('id', None)
        if not delete_id:
            return Response(status=status.HTTP_204_NO_CONTENT)
        obj = models.Href.objects.filter(id=delete_id).first()
        if obj:
            obj.delete()
            return JsonResponse({
                'status': 200,
                'msg': '删除成功',
            })
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

    # 获取单个链接信息
    @action(methods=['get'], detail=False)
    @csrf_exempt
    def single_href(self, request, *args, **kwargs):
        query_name = request.data.get('name', None)
        print(query_name)
        if not query_name:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            href = models.Href.objects.all().filter(name=query_name)
            serializer = HrefInfoModelSerializer(instance=href, many=True)
            print(serializer.data)
            return JsonResponse({
                'code': 200,
                'msg': '查询成功',
                'data': serializer.data
            })

    # 修改信息
    @action(methods=['put'], detail=False)
    @csrf_exempt
    def edit_href(self, request, *args, **kwargs):
        id = request.data.get('id', None)
        if id:
            obj = models.Href.objects.filter(id=id).first()
            serializer = HrefInfoModelSerializer(instance=obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
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
