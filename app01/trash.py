from __future__ import unicode_literals
import json
import os
from datetime import datetime
from django.core.cache import cache
from django.core.files.uploadedfile import InMemoryUploadedFile
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging
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
from .extensions.auth import JwtQueryParamsAuthentication
from .serializers import AlgorithmModelSerializer, BookInfoModelSerializer, HrefInfoModelSerializer, \
    CountDownModelSerializer, AchievementModelSerializer, \
    NewsModelSerializer, CarouselModelSerializer, SourceModelSerializer, UserModelSerializer, ArticleModelSerializer
from .utils import get_token
from bs4 import BeautifulSoup
import urllib


class MyPag(PageNumberPagination):
    page_size_query_param = "max_page"
    page_query_param = "page"


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


class AlgorithmViewSet(ModelViewSet):
    parser_classes = [JSONParser, FormParser]
    """视图集"""
    queryset = models.Algorithm.objects.all()
    serializer_class = AlgorithmModelSerializer
    # 搜索
    search_fields = ('id')

    # 添加种类
    @action(methods=['post'], detail=False)
    @csrf_exempt
    def add_algorithm(self, request, *args, **kwargs):
        name = request.data.get('name', None)
        if name:
            print(name)
            obj = models.Algorithm.objects.filter(name=name).first()
            if obj:
                return JsonResponse({
                    'status': 202,
                    'msg': '已经存在此算法名称'
                })
            else:
                serializer = AlgorithmModelSerializer(data=request.data)
                print(request.data)
                print(serializer)
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
        pass

    # 删除算法
    @action(methods=['delete'], detail=False)
    @csrf_exempt
    def deleteAlgorithm(self, request, *args, **kwargs):
        delete_id = request.data.get('id', None)
        if not delete_id:
            return Response(status=status.HTTP_404_NOT_FOUND)
        obj = models.Algorithm.objects.filter(id=delete_id).first()
        if obj:
            obj.delete()
            return JsonResponse({
                'status': 200,
                'msg': '删除成功',
            })
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

    # 修改信息
    @action(methods=['put'], detail=False)
    @csrf_exempt
    def edit_algorithm(self, request, *args, **kwargs):
        id = request.data.get('id', None)
        if id:
            name = request.data.get('name', None)
            if not name:
                return Response(status.HTTP_204_NO_CONTENT)
            else:
                obj = models.Algorithm.objects.filter(id=id).first()
                obj.name = name
                obj.save()
                return JsonResponse({
                    'status': 200,
                    'msg': '更新成功',
                })
        else:
            return Response(status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False)
    def getAll(self, request, *args, **kwargs):
        obj = models.Algorithm.objects.all()
        ser = AlgorithmModelSerializer(instance=obj, many=True)
        return JsonResponse({
            'status': 200,
            'msg': '获取数据成功',
            'data': ser.data
        })
        # if obj:
        # else:
        #     return JsonResponse({
        #         'status': 201,
        #         'msg': '获取失败',
        #     })


class CountDownViewSet(ModelViewSet):
    parser_classes = [JSONParser, FormParser]
    """视图集"""
    queryset = models.CountDownSign.objects.all()
    serializer_class = CountDownModelSerializer
    # 搜索
    search_fields = ('id', 'name', 'sign', 'date')

    @action(methods=['get'], detail=False)
    def getAll(self, request, *args, **kwargs):
        obj = models.CountDownSign.objects.all().order_by('date')
        ser = CountDownModelSerializer(instance=obj, many=True)
        return JsonResponse({
            'status': 200,
            'msg': '获取数据成功',
            'data': ser.data
        })
        # if obj:
        # else:
        #     return JsonResponse({
        #         'status': 201,
        #         'msg': '获取失败',
        #     })

    @action(methods=['post'], detail=False)
    def getSE(self, request, *args, **kwargs):
        start = request.data.get('start', None)
        end = request.data.get('end', None)
        if start and end:
            obj = models.CountDownSign.objects.filter(date__range=(start, end))

            if obj:
                ser = CountDownModelSerializer(instance=obj, many=True)
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

    # 添加倒计时
    @action(methods=['post'], detail=False)
    @csrf_exempt
    def add_countDown(self, request, *args, **kwargs):
        name = request.data.get('name', None)
        print(request.data)
        if name:
            obj = models.CountDownSign.objects.filter(name=name).first()
            if obj:
                return JsonResponse({
                    'status': 202,
                    'msg': '已经存在此竞赛名称'
                })
            else:
                date = request.data['date']
                name = request.data['name']
                sign = request.data['sign']
                request.data['date'] = '2021-02-25'
                # request.data['date'] = datetime.date.today().strftime('%y-%m-%d')
                serializer = CountDownModelSerializer(data=request.data)
                models.CountDownSign.objects.create(date=date, name=name, sign=sign)
                return JsonResponse({
                    'status': 200,
                    'msg': '添加成功'
                })
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

    # 删除倒计时
    @action(methods=['delete'], detail=False)
    @csrf_exempt
    def multiple_delete(self, request, *args, **kwargs):
        count = 0
        delete_id = request.data.get('id', None)
        if not delete_id:
            return Response(status=status.HTTP_404_NOT_FOUND)
        for i in delete_id.split(','):
            obj = models.Algorithm.objects.filter(id=i).first()
            if obj:
                obj.delete()
                count = count + 1
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)
        return JsonResponse({
            'code': 200,
            'msg': '删除成功',
            'num': count
        })

    # 修改倒计时
    @action(methods=['put'], detail=False)
    @csrf_exempt
    def edit_count(self, request, *args, **kwargs):
        id = request.data.get('id', None)
        if id:
            obj = models.CountDownSign.objects.get(id=id)
            ser = CountDownModelSerializer(instance=obj, data=request.data)
            if ser.is_valid(raise_exception=True):
                ser.save()
                return JsonResponse({
                    'status': 200,
                    'msg': '更新成功',
                })
            else:
                return JsonResponse({
                    'status': 202,
                    'msg': '修改数据不合法'
                })
        else:
            return Response(status.HTTP_204_NO_CONTENT)


# class CompetitionViewSet(ModelViewSet):
#     parser_classes = [JSONParser, FormParser]
#     """视图集"""
#     queryset = models.Competition.objects.all()
#     serializer_class = CompetitionModelSerializer
#     # 搜索
#     search_fields = ('id', 'name', 'instruction')
#
#     # 添加竞赛
#     @action(methods=['post'], detail=False)
#     @csrf_exempt
#     def add_competition(self, request, *args, **kwargs):
#         name = request.data.get('name', None)
#         if name:
#             obj = models.Competition.objects.filter(name=name).first()
#             if obj:
#                 return JsonResponse({
#                     'status': '1001',
#                     'msg': '已经存在此竞赛名称'
#                 })
#             else:
#                 serializer = CompetitionModelSerializer(data=request.data)
#                 if serializer.is_valid():
#                     serializer.save()
#                     return JsonResponse({
#                         'status': '1000',
#                         'msg': '添加成功'
#                     })
#                 else:
#                     return JsonResponse({
#                         'status': '1002',
#                         'msg': '插入数据不合法'
#                     })
#         else:
#             return Response(status=status.HTTP_204_NO_CONTENT)
#
#     # 删除倒计时
#     @action(methods=['delete'], detail=False)
#     @csrf_exempt
#     def multiple_delete(self, request, *args, **kwargs):
#         count = 0
#         delete_id = request.data.get('id', None)
#         if not delete_id:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         for i in delete_id.split(','):
#             obj = models.Competition.objects.filter(id=i).first()
#             if obj:
#                 obj.delete()
#                 count = count + 1
#             else:
#                 return Response(status=status.HTTP_204_NO_CONTENT)
#         return JsonResponse({
#             'code': 200,
#             'msg': '删除成功',
#             'num': count
#         })
#
#     # 修改倒计时
#     @action(methods=['put'], detail=False)
#     @csrf_exempt
#     def edit_count(self, request, *args, **kwargs):
#         id = request.data.get('id', None)
#         if id:
#             obj = models.Competition.objects.get(id=id)
#             ser = CompetitionModelSerializer(instance=obj, data=request.data)
#             if ser.is_valid():
#                 ser.save()
#                 return JsonResponse({
#                     'status': '200',
#                     'msg': '更新成功',
#                 })
#             else:
#                 return JsonResponse({
#                     'status': '201',
#                     'msg': '更新数据不合法'
#                 })
#         else:
#             return Response(status.HTTP_204_NO_CONTENT)


# class TeamViewSet(ModelViewSet):
#     parser_classes = [JSONParser, FormParser]
#     """视图集"""
#     queryset = models.TeamIntroduction.objects.all()
#     serializer_class = TeamModelSerializer
#     # 搜索
#     search_fields = ('id', 'content')
#
#     # 修改介绍
#     @action(methods=['put'], detail=False)
#     @csrf_exempt
#     def edit_introduction(self, request, *args, **kwargs):
#         id = request.data.get('id', None)
#         if id:
#             obj = models.TeamIntroduction.objects.get(id=id)
#             ser = TeamModelSerializer(instance=obj, data=request.data)
#             if ser.is_valid():
#                 ser.save()
#                 return JsonResponse({
#                     'code': 200,
#                     'msg': '更新成功',
#                 })
#             else:
#                 return JsonResponse({
#                     'status': '1002',
#                     'msg': '修改数据不合法'
#                 })
#         else:
#             return Response(status.HTTP_204_NO_CONTENT)


class AchievementViewSet(ModelViewSet):
    parser_classes = [JSONParser, FormParser]
    """视图集"""
    queryset = models.Achievement.objects.all()
    serializer_class = AchievementModelSerializer
    # 搜索
    search_fields = ('id', 'coach', 'date', 'reward')

    # 添加竞赛
    @action(methods=['post'], detail=False)
    @csrf_exempt
    def add_competition(self, request, *args, **kwargs):
        name = request.data.get('name', None)
        if name:
            print(name)
            obj = models.Achievement.objects.filter(name=name).first()
            if obj:
                return JsonResponse({
                    'status': '1001',
                    'msg': '已经存在此竞赛名称'
                })
            else:
                serializer = AchievementModelSerializer(data=request.data)
                print(request.data)
                print(serializer)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse({
                        'status': '1000',
                        'msg': '添加成功'
                    })
                else:
                    return JsonResponse({
                        'status': '1002',
                        'msg': '插入数据不合法'
                    })
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

    # 删除倒计时
    @action(methods=['delete'], detail=False)
    @csrf_exempt
    def multiple_delete(self, request, *args, **kwargs):
        count = 0
        delete_id = request.data.get('id', None)
        if not delete_id:
            return Response(status=status.HTTP_404_NOT_FOUND)
        for i in delete_id.split(','):
            obj = models.Achievement.objects.filter(id=i).first()
            if obj:
                obj.delete()
                count = count + 1
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)
        return JsonResponse({
            'code': 200,
            'msg': '删除成功',
            'num': count
        })

    # 修改倒计时
    @action(methods=['put'], detail=False)
    @csrf_exempt
    def edit_count(self, request, *args, **kwargs):
        id = request.data.get('id', None)
        if id:
            obj = models.Achievement.objects.get(id=id)
            ser = AchievementModelSerializer(instance=obj, data=request.data)
            if ser.is_valid():
                ser.save()
                return JsonResponse({
                    'code': 200,
                    'msg': '更新成功',
                })
            else:
                return JsonResponse({
                    'status': '1002',
                    'msg': '修改数据不合法'
                })
        else:
            return Response(status.HTTP_204_NO_CONTENT)


# ?page=1&max_page=6
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
        # if obj:
        # else:
        #     return JsonResponse({
        #         'status': 201,
        #         'msg': '获取失败',
        #     })

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
        # if obj:
        # else:
        #     return JsonResponse({
        #         'status': 201,
        #         'msg': '获取失败',
        #     })

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


class CarouselViewSet(ModelViewSet):
    parser_classes = [MultiPartParser, JSONParser, FormParser]
    """视图集"""
    queryset = models.Carousel.objects.all()
    serializer_class = CarouselModelSerializer
    # 搜索
    search_fields = ('id', 'image')

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
            logging.basicConfig(level=logging.INFO, stream=sys.stdout)
            secret_id = 'AKIDd4E7krNNktpW7kaF8k71hFYbnlS4IZR1'  # 替换为用户的 secretId
            secret_key = 'T6VeqNNAgmkaEfrRovVtzymaFj4JrBG5'  # 替换为用户的 secretKey
            region = 'ap-nanjing'  # 替换为用户的 Region
            token = None  # 使用临时密钥需要传入 Token，默认为空，可不填
            scheme = 'http'  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
            config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
            client = CosS3Client(config)
            response = client.put_object(
                Bucket='carousel-1254029770',
                Body=file,
                Key=filename,
                ContentType=typefile,
                StorageClass='STANDARD',
                EnableMD5=False
            )
            # print(response['ETag'])
            if (response['ETag']):
                baseurl = 'https://carousel-1254029770.cos.ap-nanjing.myqcloud.com/'
                fileUrl = baseurl + filename
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
            logging.basicConfig(level=logging.INFO, stream=sys.stdout)
            secret_id = 'AKIDd4E7krNNktpW7kaF8k71hFYbnlS4IZR1'  # 替换为用户的 secretId
            secret_key = 'T6VeqNNAgmkaEfrRovVtzymaFj4JrBG5'  # 替换为用户的 secretKey
            region = 'ap-nanjing'  # 替换为用户的 Region
            token = None  # 使用临时密钥需要传入 Token，默认为空，可不填
            scheme = 'http'  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
            config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
            client = CosS3Client(config)
            print(obj.filename)
            response = client.delete_object(
                Bucket='carousel-1254029770',
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


class ResourceViewSet(ModelViewSet):
    parser_classes = [MultiPartParser, JSONParser, FormParser]
    """视图集"""
    queryset = models.Source.objects.all()
    serializer_class = SourceModelSerializer
    # 搜索
    search_fields = ('id')

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

    # # @action(methods=['get'], detail=False)
    # @csrf_exempt
    # def get_resource_Download(self, request, *args, **kwargs):
    #     file_path = os.path.join(os.getcwd(), 'static/files/', 'img.png').replace('\\', '/')
    #     # file = open(file_path, "r", encoding='utf-8')
    #     # print(file)
    #     # response = HttpResponse(file, content_type='application/octet-stream')
    #     # print(1)
    #     # response['Content-Disposition'] = "attachment; filename= {}".format(str(obj.file))
    #     # # response['Content-Disposition'] = 'attachment; filename=NameOfFile'
    #     # print(2)
    #     file = open(file_path, 'rb')
    #     response = FileResponse(file)
    #     # response = StreamingHttpResponse(file)
    #     response['Content-Type'] = 'image/jpeg'
    #     # response['Content-Disposition'] = 'attachment;filename={}'.format('str(obj.file)')
    #     return response
    #     # id = request.data.get('id', None)
    #     # if id:
    #     #     print(id)
    #     #     obj = models.Source.objects.filter(id=id).first()
    #     #     if obj:
    #     #         file_path = os.path.join(os.getcwd(), 'static/', str(obj.file)).replace('\\', '/')
    #     #         # file = open(file_path, "r", encoding='utf-8')
    #     #         # print(file)
    #     #         # response = HttpResponse(file, content_type='application/octet-stream')
    #     #         # print(1)
    #     #         # response['Content-Disposition'] = "attachment; filename= {}".format(str(obj.file))
    #     #         # # response['Content-Disposition'] = 'attachment; filename=NameOfFile'
    #     #         # print(2)
    #     #         file = open(file_path, 'rb')
    #     #         response = FileResponse(file)
    #     #         # response = StreamingHttpResponse(file)
    #     #         response['Content-Type'] = 'application/octet-stream'
    #     #         response['Content-Disposition'] = 'attachment;filename={}'.format(str(obj.file))
    #     #
    #     #         return response
    #     #     else:
    #     #         return Response(status=status.HTTP_204_NO_CONTENT)
    #     # else:
    #     #     return Response(status=status.HTTP_204_NO_CONTENT)

    # 添加资源
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
            logging.basicConfig(level=logging.INFO, stream=sys.stdout)
            secret_id = 'AKIDd4E7krNNktpW7kaF8k71hFYbnlS4IZR1'  # 替换为用户的 secretId
            secret_key = 'T6VeqNNAgmkaEfrRovVtzymaFj4JrBG5'  # 替换为用户的 secretKey
            region = 'ap-guangzhou'  # 替换为用户的 Region
            token = None  # 使用临时密钥需要传入 Token，默认为空，可不填
            scheme = 'http'  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
            config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
            client = CosS3Client(config)
            response = client.put_object(
                Bucket='costest-1254029770',
                Body=file,
                Key=filename,
                ContentType=type,
                StorageClass='STANDARD',
                EnableMD5=False
            )
            if (response['ETag']):
                baseurl = 'https://costest-1254029770.cos.ap-guangzhou.myqcloud.com/'
                fileUrl = baseurl + filename
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
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        secret_id = 'AKIDd4E7krNNktpW7kaF8k71hFYbnlS4IZR1'  # 替换为用户的 secretId
        secret_key = 'T6VeqNNAgmkaEfrRovVtzymaFj4JrBG5'  # 替换为用户的 secretKey
        region = 'ap-guangzhou'  # 替换为用户的 Region
        token = None  # 使用临时密钥需要传入 Token，默认为空，可不填
        scheme = 'http'  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
        config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
        client = CosS3Client(config)
        response = client.delete_object(
            Bucket='costest-1254029770',
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

    # @action(methods=['post'], detail=False)
    # @csrf_exempt
    # def download_resource(self, request, *args, **kwargs):
    #     id = request.data.get('id')
    #     obj = models.Source.objects.filter(id=id).first()
    #     # res = requests.get(obj.file)
    #     res = requests.get(obj.file)
    #     content_type = res.headers['Content-Type']
    #     with open('tmp-file', "wb") as file:
    #         file.write(res.content)
    #     with open('tmp-file', "rb") as file:
    #         return FileResponse(file)


class UserViewSet(ModelViewSet):
    parser_classes = [MultiPartParser, JSONParser, FormParser]
    """视图集"""
    queryset = models.User.objects.all()
    serializer_class = UserModelSerializer
    # 搜索
    search_fields = ('id')

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
                logging.basicConfig(level=logging.INFO, stream=sys.stdout)
                secret_id = 'AKIDd4E7krNNktpW7kaF8k71hFYbnlS4IZR1'  # 替换为用户的 secretId
                secret_key = 'T6VeqNNAgmkaEfrRovVtzymaFj4JrBG5'  # 替换为用户的 secretKey
                region = 'ap-nanjing'  # 替换为用户的 Region
                token = None  # 使用临时密钥需要传入 Token，默认为空，可不填
                scheme = 'http'  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
                config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
                client = CosS3Client(config)
                baseurl = 'https://user-1254029770.cos.ap-nanjing.myqcloud.com/'

                if obj.uid != '':
                    print(obj.uid)
                    response = client.delete_object(
                        Bucket='user-1254029770',
                        Key=obj.uid
                    )
                response = client.put_object(
                    Bucket='user-1254029770',
                    Body=file,
                    Key=filename,
                    ContentType=type,
                    StorageClass='STANDARD',
                    EnableMD5=False
                )
                if (response['ETag']):
                    fileUrl = baseurl + filename
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


# class CommentViewSet(ModelViewSet):
#     parser_classes = [MultiPartParser, JSONParser, FormParser]
#     """视图集"""
#     queryset = models.Comment.objects.all()
#     serializer_class = CommentModelSerializer
#     # 搜索
#     search_fields = ('id')
#
#     @action(methods=['post'], detail=False)
#     @csrf_exempt
#     def add_comment(self, request, *args, **kwargs):
#         name = request.data.get('name', None)
#         if name:
#             print(name)
#             obj = models.Comment.objects.filter(name=name).first()
#             if obj:
#                 return JsonResponse({
#                     'status': '1001',
#                     'msg': '已经存在此用户名称'
#                 })
#             else:
#                 serializer = CommentModelSerializer(data=request.data)
#
#                 if serializer.is_valid():
#                     serializer.save()
#                     return JsonResponse({
#                         'status': '1000',
#                         'msg': '添加成功'
#                     })
#                 else:
#                     return JsonResponse({
#                         'status': '1002',
#                         'msg': '插入数据不合法'
#                     })
#         else:
#             return Response(status=status.HTTP_204_NO_CONTENT)
#
#     # 删除用户
#     @action(methods=['delete'], detail=False)
#     @csrf_exempt
#     def multiple_delete(self, request, *args, **kwargs):
#         delete_id = request.data.get('id', None)
#         if not delete_id:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         else:
#             obj = models.Comment.objects.filter(id=delete_id).first()
#             if obj:
#                 obj.delete()
#             else:
#                 return Response(status=status.HTTP_204_NO_CONTENT)
#         return JsonResponse({
#             'code': 200,
#             'msg': '删除成功',
#         })


# class ACMerViewSet(ModelViewSet):
#     parser_classes = [MultiPartParser, JSONParser, FormParser]
#     # authentication_classes = [JwtQueryParamsAuthentication]
#     """视图集"""
#     queryset = models.ACMer.objects.all()
#     serializer_class = ACMerModelSerializer
#     # 搜索
#     search_fields = ('id')
#
#     @action(methods=['post'], detail=False)
#     @csrf_exempt
#     def add_acmer(self, request, *args, **kwargs):
#         serializer = ACMerModelSerializer(data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse({
#                 'status': '1000',
#                 'msg': '添加成功'
#             })
#         else:
#             return JsonResponse({
#                 'status': '1002',
#                 'msg': '插入数据不合法'
#             })
#
#     @action(methods=['post'], detail=False)
#     @csrf_exempt
#     def getByDate(self, request, *args, **kwargs):
#         year = request.data.get('year', None)
#         if year:
#             obj = models.CountDownSign.objects.filter(year=year).all()
#             if obj:
#                 ser = CountDownModelSerializer(instance=obj, many=True)
#                 print(ser.data)
#                 return JsonResponse({
#                     'code': '200',
#                     'msg': '获取数据成功',
#                     'data': ser.data
#                 })
#             else:
#                 return JsonResponse({
#                     'code': '1002',
#                     'msg': '获取失败',
#                 })
#         else:
#             return Response(status=status.HTTP_204_NO_CONTENT)
#
#     # 删除用户
#     @action(methods=['delete'], detail=False)
#     @csrf_exempt
#     def multiple_delete(self, request, *args, **kwargs):
#         delete_id = request.data.get('id', None)
#         if not delete_id:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         else:
#             obj = models.ACMer.objects.filter(id=delete_id).first()
#             if obj:
#                 obj.delete()
#             else:
#                 return Response(status=status.HTTP_204_NO_CONTENT)
#         return JsonResponse({
#             'code': 200,
#             'msg': '删除成功',
#         })
#
#     @action(methods=['get'], detail=False)
#     def getAll(self, request, *args, **kwargs):
#         obj = models.ACMer.objects.all().order_by('year')
#         ser = ACMerModelSerializer(instance=obj, many=True)
#         return JsonResponse({
#             'status': 200,
#             'msg': '获取数据成功',
#             'data': ser.data
#         })
#         # if obj:
#         # else:
#         #     return JsonResponse({
#         #         'status': 201,
#         #         'msg': '获取失败',
#         #     })
#
#     #
#     @action(methods=['put'], detail=False)
#     @csrf_exempt
#     def edit_acmer(self, request, *args, **kwargs):
#         id = request.data.get('id', None)
#         if id:
#             obj = models.ACMer.objects.get(id=id)
#             ser = ACMerModelSerializer(instance=obj, data=request.data)
#             if ser.is_valid():
#                 ser.save()
#                 return JsonResponse({
#                     'code': 200,
#                     'msg': '更新成功',
#                 })
#             else:
#                 return JsonResponse({
#                     'status': '1002',
#                     'msg': '修改数据不合法'
#                 })
#         else:
#             return Response(status.HTTP_204_NO_CONTENT)

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

# router = SimpleRouter()  # 创建路由器(路由器只能结束视图集一起使用) 默认只为标准了增删改查行为生成路由信息,如果想让自定义的行为也生成路由需要在自定义行为上用action装饰进行装饰
# router.register(r'books', views.BookViewSet)  # 注册路由
# router.register(r'href', views.HrefViewSet)  # 注册路由
# router.register(r'algorithm', views.AlgorithmViewSet)  # 注册路由
# router.register(r'countDown', views.CountDownViewSet)  # 注册路由
# # router.register(r'competition', views.CompetitionViewSet)  # 注册路由
# # router.register(r'team', views.TeamViewSet)  # 注册路由
# router.register(r'achievement', views.AchievementViewSet)  # 注册路由
# router.register(r'news', views.NewsViewSet)  # 注册路由
# router.register(r'carousel', views.CarouselViewSet)  # 注册路由
# router.register(r'resource', views.ResourceViewSet)  # 注册路由
# # router.register(r'acmer', views.ACMerViewSet)  # 注册路由
# router.register(r'article', views.ArticleViewSet)  # 注册路由
# # router.register(r'comment', views.CommentViewSet)  # 注册路由
# router.register(r'login', viewsUtils)  # 注册路由
# router.register(r'user', UserView.UserViewSet)  # 注册路由
# urlpatterns += router.urls  # 把生成好的路由拼接到urlpatterns
