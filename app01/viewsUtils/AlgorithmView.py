from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FormParser
from app01 import models
from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet
from ..serializers import AlgorithmModelSerializer


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
