from __future__ import unicode_literals
import json
from django.views.decorators.csrf import csrf_exempt
from lxml import etree
from django.http import JsonResponse
import requests
import random
from bs4 import BeautifulSoup


def daily_ac(request):
    if request.method == "GET":
        url = "https://www.acwing.com/problem/content/" + str(random.randint(1, 234)) + "/"
        response = requests.get(url)
        title = ''
        txt = ''
        code = 201
        if response.status_code == 200:
            code = 200
            soup = BeautifulSoup(response.text).find_all(name="div", attrs={"data-tab": "preview-tab-content"})
            txt = str('"' + str(soup[0]).replace('"', "'") + '"')
            title = \
                BeautifulSoup(response.text).find_all(name="div",
                                                      attrs={"class": 'nice_font problem-content-title'})[
                    0].text
            title = str(title).replace(' ', '')
            title = title[title.find('.') + 1:]
        return JsonResponse({
            'status': code,
            'msg': '获取题目成功',
            'data': txt,
            'title': title,
            'url': url
        })


@csrf_exempt
def getMeaning(request):
    if request.method == "POST":
        json_str = request.body  # 属性获取最原始的请求体数据
        json_dict = json.loads(json_str)  # 将原始数据转成字典格式
        key = json_dict.get("key", None)  # 获取数据
        url = 'http://dict.youdao.com/search?q=' + key + '&keyfrom=new-fanyi.smartResult'
        r = requests.get(url)
        r.encoding = r.apparent_encoding
        info = ''
        if r.status_code == 200:
            text = r.text
            doc = etree.HTML(text)
            res = doc.xpath('//*[@id="phrsListTab"]/div[2]/ul/li/text()')
            return JsonResponse({
                'status': 200,
                'data': res
            })
        else:
            return JsonResponse({
                'status': 201,
                'data': '未查询到'
            })
    else:
        return JsonResponse({
            'status': '404'
        })

    # 获取四六级单词


def getWord(request):
    if request.method == 'GET':
        words = []
        meaning = []
        choice = random.choice([(11, 226), (12, 105), (122, 35), (123, 25)])
        url = "http://word.iciba.com/?action=words&class=" + str(choice[0]) + "&course=" + str(
            random.randint(1, choice[1]))
        r = requests.get(url)
        r.encoding = r.apparent_encoding
        if r.status_code == 200:
            text = r.text
            doc = etree.HTML(text)
            words = doc.xpath('//*[@class="word_main_list"]/li/div[@class="word_main_list_w"]/span//text()')
            meaning = doc.xpath('//*[@class="word_main_list"]/li/div[@class="word_main_list_s"]/span//text()')
            li = []
            for i in range(int(len(words) / 2)):
                dic = {'words': words[i], 'meaning': meaning[i]}
                li.append(dic)
            return JsonResponse({'data': li,
                                 'status': 200})
        else:
            return JsonResponse({
                'data': '',
                'status': 201})
