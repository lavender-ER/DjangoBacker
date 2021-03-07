from rest_framework import serializers, status
from rest_framework.response import Response

from .models import Href, Book, Algorithm, CountDownSign, Achievement, News, Carousel, \
    Source, User, Article
from rest_framework.pagination import PageNumberPagination


class MyPageNumberPagination(PageNumberPagination):
    page_size = 5
    max_page_size = 5
    page_size_query_param = 'size'
    page_query_param = 'page'


class BookInfoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    def create(self, validated_data):
        return Book.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        # instance.date = datetime.datetime.today()
        instance.publisher = validated_data.get('publisher', instance.publisher)
        instance.save()
        return instance


class HrefInfoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Href
        fields = '__all__'

    def create(self, validated_data):
        return Href.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.url = validated_data.get('url', instance.url)
        instance.save()
        return instance


class AlgorithmModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Algorithm
        fields = '__all__'

    def create(self, validated_data):
        return Algorithm.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class CountDownModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountDownSign
        fields = '__all__'

    def create(self, validated_data):
        return CountDownSign.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.date = validated_data.get('date', instance.date)
        instance.sign = validated_data.get('sign', instance.sign)
        instance.save()
        return instance


# class CompetitionModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Competition
#         fields = '__all__'
#
#     def create(self, validated_data):
#         return Competition.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.instruction = validated_data.get('instruction', instance.instruction)
#         instance.save()
#         return instance


# class TeamModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TeamIntroduction
#         fields = '__all__'
#
#     def create(self, validated_data):
#         return TeamIntroduction.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.content = validated_data.get('content', instance.content)
#         instance.save()
#         return instance


class AchievementModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = '__all__'

    def create(self, validated_data):
        return Achievement.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.date = validated_data.get('date', instance.date)
        instance.team = validated_data.get('team', instance.team)
        instance.reward = validated_data.get('reward', instance.reward)
        instance.coach = validated_data.get('coach', instance.coach)
        instance.ACMer = validated_data.get('ACMer', instance.ACMer)
        instance.save()
        return instance


class NewsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'

    def create(self, validated_data):
        return News.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.author = validated_data.get('author', instance.author)
        instance.date = validated_data.get('date', instance.date)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance


class CarouselModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carousel
        fields = '__all__'

    def create(self, validated_data):
        return Carousel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.title)
        instance.filename = validated_data.get('filename', instance.filename)
        # instance.note = validated_data.get('note', instance.note)
        instance.save()
        return instance


class SourceModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = '__all__'

    def create(self, validated_data):
        return Source.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.uploader = validated_data.get('uploader', instance.uploader)
        instance.date = validated_data.get('date', instance.date)
        instance.memory = validated_data.get('memory', instance.memory)
        instance.name = validated_data.get('name', instance.name)
        instance.file = validated_data.get('file', instance.file)
        instance.desc = validated_data.get('desc', instance.desc)
        instance.uid = validated_data.get('uid', instance.uid)
        instance.save()
        return instance


# 这里
class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.pwd = validated_data.get('pwd', instance.pwd)
        # instance.sex = validated_data.get('sex', instance.sex)
        # instance.birth = validated_data.get('birth', instance.birth)
        instance.date = validated_data.get('date', instance.date)
        # instance.start = validated_data.get('start', instance.start)
        # instance.follow = validated_data.get('follow', instance.follow)
        # instance.fans = validated_data.get('fans', instance.fans)
        instance.articles = validated_data.get('articles', instance.articles)
        instance.note = validated_data.get('note', instance.note)
        # instance.head = validated_data.get('head', instance.head)
        instance.root = validated_data.get('root', instance.root)
        instance.save()
        return instance


class ArticleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

    def create(self, validated_data):
        return Article.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.content = validated_data.get('content', instance.content)
        instance.title = validated_data.get('title', instance.title)
        instance.author = validated_data.get('author', instance.author)
        instance.date = validated_data.get('date', instance.date)
        # instance.last_alter = validated_data.get('last_alter', instance.last_alter)
        instance.algorithm = validated_data.get('algorithm', instance.algorithm)
        instance.stars = validated_data.get('stars', instance.stars)
        instance.author_id = validated_data.get('author_id', instance.author_id)
        instance.desc = validated_data.get('desc', instance.desc)
        # instance.algorithm_id = validated_data.get('algorithm_id', instance.algorithm_id)
        instance.save()
        return instance

# class CommentModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = '__all__'
#
#     def create(self, validated_data):
#         return Comment.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.author = validated_data.get('author', instance.author)
#         instance.date = validated_data.get('date', instance.date)
#         instance.content = validated_data.get('content', instance.content)
#         instance.target = validated_data.get('target', instance.target)
#         instance.save()
#         return instance


# class ACMerModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ACMer
#         fields = '__all__'
#
#     def create(self, validated_data):
#         return ACMer.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.year = validated_data.get('year', instance.year)
#         instance.name = validated_data.get('name', instance.name)
#         instance.head = validated_data.get('head', instance.head)
#         # instance.imageUrl = validated_data.get('imageUrl', instance.imageUrl)
#         instance.save()
#         return instance
