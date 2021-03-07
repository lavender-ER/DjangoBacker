from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from app01 import models
from django.http import HttpResponse, JsonResponse, FileResponse
from rest_framework.viewsets import ModelViewSet
from ..extensions.auth import JwtQueryParamsAuthentication
from ..serializers import CountDownModelSerializer
from ..utils import get_token


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
