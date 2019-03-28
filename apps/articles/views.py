from rest_framework import mixins,filters,viewsets
from rest_framework.pagination import PageNumberPagination,CursorPagination,LimitOffsetPagination
import datetime
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Category,Article,Tag
from .serializer import CategorysSer,ArticlesSer,TagsSer,HotArticlesSer,CardArticlesSer,TimeArticlesSer,ArticlesDetailSer

class ArticlesPage(PageNumberPagination):
    #cursor_query_param = 'cursor'
    page_size = 6
    ordering = '-create_time'
    page_size_query_param = 'size'
    max_page_size = 10

class CategorysViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    """
    文章分类列表
    """
    queryset = Category.objects.all()
    serializer_class = CategorysSer

class TagsViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    """
    标签列表
    """
    queryset = Tag.objects.all()
    serializer_class = TagsSer

class HotArticleSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    """
    热读文章，前5个
    """
    queryset = Article.objects.filter(status=1).order_by("-views")[:5]
    serializer_class = HotArticlesSer


class CardArticleSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    """
    置顶轮播
    """
    queryset = Article.objects.filter(top=1)
    serializer_class = CardArticlesSer

def lastMonth():
    today = datetime.date.today()
    this_month = datetime.datetime(today.year,today.month,1)
    last_month = this_month-datetime.timedelta(days=1)
    return last_month


class TimeLineset(mixins.ListModelMixin,viewsets.GenericViewSet):
    """
    时间线,按年月分组
    """
    queryset = Article.objects.filter(status=1)
    serializer_class = TimeArticlesSer

    def list(self, request, *args, **kwargs):

        """
        这里的一段循环就是为了方便vue适配三层时间线，
        而django模板只需要一个regroup就行了，心塞塞

        """
        queryset = Article.objects.filter(status=1).order_by("-create_time")[:50]
        ser = TimeArticlesSer(instance=queryset,many=True)
        data = {}
        year = {}
        month = {}
        day = {}



        for i,d in enumerate(ser.data):
            data[i+1]=d
        print(data)
        for (d, x) in data.items():
            #print("key:"+str(d)+",value:"+str(x))
            day[x['create_time']] = x
            month[x['month']+"月"] = day#如果不加字符串的话，数据会自动按数字从小到大排序的
            print(x['year'])
            year[str(x['year'])+"年"] = month
            # a = x['month']
            if d < len(data):
                if x['month'] != data[d+1]['month']:
                    day = {}
                if x['year'] != data[d+1]['year']:
                    month = {}
                    day = {}



        return Response(year,status=status.HTTP_200_OK)




class ArticlesViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    """
    文章列表页, 分页， 搜索， 过滤
    """
    queryset = Article.objects.filter(status=1).order_by("-create_time")
    serializer_class = ArticlesSer
    pagination_class = ArticlesPage
    filter_backends = (DjangoFilterBackend,filters.SearchFilter)
    filter_fields = ('category','tags','author')
    search_fields=('title','detail')

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ArticlesDetailSer
        return ArticlesSer

    def retrieve(self, request, *args, **kwargs):
        #统计阅读量
        obj = self.get_object()
        obj.views +=1
        obj.save()
        serializer = self.get_serializer(obj)
        return Response(serializer.data)


