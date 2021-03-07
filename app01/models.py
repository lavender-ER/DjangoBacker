from django.db import models
from django.utils import timezone


class News(models.Model):
    title = models.CharField(max_length=100)  # 新闻标题
    author = models.CharField(max_length=50)  # 发布人 操作者
    date = models.DateTimeField(auto_now_add=True)  # 发表日期  自动添加
    content = models.TextField(max_length=12321)  # 文章正文


# 友情链接
class Href(models.Model):
    name = models.CharField(max_length=100, blank=True)  # 名称
    url = models.CharField(max_length=100, blank=True)  # 链接地址


# 推荐书籍
class Book(models.Model):
    name = models.CharField(max_length=1000)  # 书籍名称
    publisher = models.CharField(max_length=1000)  # 出版社名称
    date = models.DateTimeField(default=timezone.now)  # 添加日期


# 团队成绩
class Achievement(models.Model):
    name = models.CharField(max_length=100)  # 竞赛名称
    date = models.DateField()  # 取得时间
    team = models.CharField(max_length=100)  # 参赛队伍
    reward = models.CharField(max_length=100)  # 奖项名称
    coach = models.CharField(max_length=100)  # 教练
    ACMer = models.CharField(max_length=100)  # 队伍人员


# 用户
class User(models.Model):
    uid = models.TextField(max_length=1000)
    filename = models.TextField(max_length=1000)
    nickname = models.CharField(max_length=100, default="HNUSTACMer")  # 用户昵称
    pwd = models.CharField(max_length=120, default='123456789')
    # sex = models.CharField(max_length=10, default='男')  # 用户性别
    # birth = models.DateField(auto_created=True, default=timezone.now)  # 用户生日
    date = models.DateField(auto_created=True, default=timezone.now)  # 注册日期
    # start = models.IntegerField(default=0)  # 用户获得的星数
    follow = models.IntegerField(default=0)  # 关注的人数
    # fans = models.IntegerField(default=0)  # 粉丝数
    articles = models.IntegerField(default=0)  # 用户发表文章数
    note = models.CharField(max_length=100, default="让我们红橙作伴，活的潇潇洒洒")  # 用户格言
    # head = models.ImageField(upload_to='../static/images/', default="../staic/images/avatar_1569504708.png")  # 用户头像
    root = models.IntegerField(default=0)  # 用户的权限 默认为一般用户


# 集训队员
# class ACMer(models.Model):
#     year = models.CharField(max_length=100)  # 年级
#     name = models.CharField(max_length=100)  # coder 的姓名
#     head = models.ImageField(upload_to="media/acmer")  # coder 的照片


# 轮播图
class Carousel(models.Model):
    # note = models.CharField(max_length=100)
    image = models.TextField(max_length=1000)
    filename = models.TextField(max_length=1000)


# 文章
class Article(models.Model):
    author_id = models.IntegerField(default=0)  # 创建者id
    # algorithm_id = models.IntegerField(default=0)  # 文章类型id
    desc = models.TextField(max_length=327, default='')  # 发布文章描述
    content = models.TextField(max_length=32765)  # 发布文章内容
    title = models.CharField(max_length=100)  # 文章题目
    author = models.CharField(max_length=100)  # 默认为创建者
    date = models.DateTimeField(auto_created=True)  # 默认为创建的时间
    # last_alter = models.DateTimeField(auto_created=True, default=timezone.now)  # 默认为最后一次提交修改
    algorithm = models.CharField(max_length=20)  # 文章类型
    stars = models.IntegerField(default=0)  # 被点赞次数


# 博客种类
class Algorithm(models.Model):
    name = models.CharField(max_length=100)  # 算法名称


# 资源
class Source(models.Model):
    desc = models.TextField(max_length=1000)  # 描述
    uploader = models.CharField(max_length=100)  # 默认为操作者
    date = models.DateTimeField(default=timezone.now)  # 上传时间默认
    memory = models.IntegerField()  # 上传文件的内存大小
    name = models.CharField(max_length=100)  # 文件名称
    file = models.TextField(max_length=1000)  # 文件
    uid = models.TextField(max_length=1000)


# 博客评论
# class Comment(models.Model):
#     author = models.CharField(max_length=100)  # 默认为 发布者 外键
#     date = models.DateTimeField(auto_created=True)  # 发布时间
#     content = models.CharField(max_length=200)  # 评论内容
#     target = models.IntegerField()  # 评论针对的博文 外键


# 赛事报名
class CountDownSign(models.Model):
    name = models.CharField(max_length=1000)  # 赛事名称
    date = models.DateField()  # 赛事举行的时间
    sign = models.CharField(max_length=200)  # 报名链接

# 竞赛介绍
# class Competition(models.Model):
#     name = models.CharField(max_length=50)  # 赛事名称
#     instruction = models.CharField(max_length=5000)  # 赛事介绍


# class SpiderACMer(models.Model):
#     note = models.IntegerField()
#     name = models.CharField(max_length=100)
