from __future__ import unicode_literals
from datetime import datetime
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
from ..serializers import ArticleModelSerializer


class ArticleViewSet(ModelViewSet):
    parser_classes = [MultiPartParser, JSONParser, FormParser]
    # authentication_classes = [JwtQueryParamsAuthentication]
    """视图集"""
    queryset = models.Article.objects.all()
    serializer_class = ArticleModelSerializer
    # 搜索
    search_fields = ('id')

    # 获取所有文章和评论
    @action(methods=['post'], detail=False)
    @csrf_exempt
    def get_articles(self, request, *args, **kwargs):
        algorithm = request.data.get('algorithm', None)
        if algorithm:
            data = models.Article.objects.all()
            ser = ArticleModelSerializer(instance=data, many=True)
            return JsonResponse({
                'status': 200,
                'msg': '获取数据成功',
                'data': ser.data
            })
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=False)
    @csrf_exempt
    def get_articlesByAuthorId(self, request, *args, **kwargs):
        id = request.data.get('id', None)
        if id:
            data = models.Article.objects.filter(author_id=id)
            ser = ArticleModelSerializer(instance=data, many=True)
            return JsonResponse({
                'status': 200,
                'msg': '获取数据成功',
                'data': ser.data
            })
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=False)
    @csrf_exempt
    def get_articlesById(self, request, *args, **kwargs):
        id = request.data.get('id', None)
        if id:
            data = models.Article.objects.filter(id=id)
            ser = ArticleModelSerializer(instance=data, many=True)
            return JsonResponse({
                'status': 200,
                'msg': '获取数据成功',
                'data': ser.data
            })
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=False)
    @csrf_exempt
    def get_articlesByAlgId(self, request, *args, **kwargs):
        id = request.data.get('id', None)
        if id:
            obj = models.Algorithm.objects.filter(id=id).first()
            if obj:
                print(obj)
                data = models.Article.objects.filter(algorithm=obj.name)
                ser = ArticleModelSerializer(instance=data, many=True)
                return JsonResponse({
                    'status': 200,
                    'msg': '获取数据成功',
                    'data': ser.data
                })
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

    # 选择性获取文章
    @action(methods=['post'], detail=False)
    @csrf_exempt
    def get_articlesByCs(self, request, *args, **kwargs):
        algorithm = request.data.get('algorithm', None)
        start = request.data.get('start', None)
        end = request.data.get('end', None)
        print(algorithm + " " + start + " " + end)
        if start and end and algorithm:
            if algorithm == 'all':
                obj = models.Article.objects.filter(date__range=(start, end))
                if obj:
                    ser = ArticleModelSerializer(instance=obj, many=True)
                    return JsonResponse({
                        'status': 200,
                        'msg': '获取数据成功',
                        'data': ser.data
                    })
                else:
                    return JsonResponse({
                        'status': 201,
                        'msg': '未查询到数据',
                    })
            elif start == 'start' and end == 'end':
                obj = models.Article.objects.filter(algorithm=algorithm)
                ser = ArticleModelSerializer(instance=obj, many=True)
                return JsonResponse({
                    'status': 200,
                    'msg': '获取数据成功',
                    'data': ser.data,
                })
            else:
                obj = models.Article.objects.filter(algorithm=algorithm).filter(date__range=(start, end))
                ser = ArticleModelSerializer(instance=obj, many=True)
                return JsonResponse({
                    'status': 200,
                    'msg': '获取数据成功',
                    'data': ser.data,
                })
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

    # 添加文章
    @action(methods=['post'], detail=False)
    @csrf_exempt
    def add_article(self, request, *args, **kwargs):
        content = request.data.get('content', None)
        author_id = request.data.get('author_id', None)
        request.data['date'] = datetime.now()
        print(content)
        if content and author_id:
            serializer = ArticleModelSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                obj = models.User.objects.filter(id=author_id).first()
                obj.articles = obj.articles + 1
                obj.save()
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

    # 删除文章
    @action(methods=['delete'], detail=False)
    @csrf_exempt
    def deleteItem(self, request, *args, **kwargs):
        delete_id = request.data.get('id', None)
        if not delete_id:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            obj = models.Article.objects.filter(id=delete_id).first()
            if obj:
                obj.delete()
                return JsonResponse({
                    'status': 200,
                    'msg': '删除成功',
                })
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)

    # 修改文章
    @action(methods=['put'], detail=False)
    @csrf_exempt
    def edit_article(self, request, *args, **kwargs):
        id = request.data.get('id', None)
        if id:
            request.data['date'] = datetime.now()
            obj = models.Article.objects.get(id=id)
            ser = ArticleModelSerializer(instance=obj, data=request.data)
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

    @action(methods=['get'], detail=False)
    def topArticles(self, request, *args, **kwargs):
        obj = models.Article.objects.all().order_by('stars')[:5]
        if obj:
            ser = ArticleModelSerializer(instance=obj, many=True)
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
