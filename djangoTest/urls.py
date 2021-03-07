from django.urls import path
from app01 import views
from app01.viewsUtils import AlgorithmView, BookView, HrefView, CountDownView, NewsView, CarouselView, ResourceView, \
    ArticleView, LoginView, UserView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import SimpleRouter

urlpatterns = [
                  path('getWords/', views.getWord),
                  path('getMeaning/', views.getMeaning),
                  path('getAC/', views.daily_ac),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
router = SimpleRouter()  # 创建路由器(路由器只能结束视图集一起使用) 默认只为标准了增删改查行为生成路由信息,如果想让自定义的行为也生成路由需要在自定义行为上用action装饰进行装饰
router.register(r'books', BookView.BookViewSet)
router.register(r'href', HrefView.HrefViewSet)
router.register(r'algorithm', AlgorithmView.AlgorithmViewSet)
router.register(r'countDown', CountDownView.CountDownViewSet)
router.register(r'news', NewsView.NewsViewSet)
router.register(r'carousel', CarouselView.CarouselViewSet)
router.register(r'resource', ResourceView.ResourceViewSet)
router.register(r'article', ArticleView.ArticleViewSet)
router.register(r'login', LoginView.LoginViewSet)
router.register(r'user', UserView.UserViewSet)
urlpatterns += router.urls  # 把生成好的路由拼接到urlpatterns
