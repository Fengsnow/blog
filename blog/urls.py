"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
import os
from blog import settings
import xadmin
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter


from articles.views import ArticlesViewSet,CategorysViewSet,TagsViewSet,HotArticleSet,CardArticleSet,TimeLineset
from management.views import index


router = DefaultRouter()

#文章分类
router.register(r'category', CategorysViewSet, base_name="category")
#标签
router.register(r'tag', TagsViewSet, base_name="tag")
#热读
router.register(r'hotarticle', HotArticleSet, base_name="hotarticle")
#轮播卡片
router.register(r'cardarticle', CardArticleSet, base_name="cardarticle")
#时间线
router.register(r'timeline', TimeLineset, base_name="timeline")
#文章
router.register(r'article', ArticlesViewSet, base_name="article")


urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('api-auth/', include('rest_framework.urls')), #rdf登录认证
    path('docs/',include_docs_urls(title="文档")), #rdf文档

    path('',index,name="index"),#主页
    path('', include(router.urls)),
]
media_root = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=media_root)
