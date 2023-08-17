from allauth.account.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import upgrade_me, CategoryListView, subscribe
from news.views import PostsList, PostsDetail, SearchPostList, PostCreate, PostUpdate, PostDelete, ArticleCreate, \
    ArticleUpdate, ArticleDelete, LoginRequired, Logout

urlpatterns = [
    path('', PostsList.as_view()),
    path('<int:pk>', PostsDetail.as_view()),
    path('news/search', SearchPostList.as_view(), name='news_search'),
    path('news/create', PostCreate.as_view(), name='news_create'),
    path('news/<int:pk>/update', PostUpdate.as_view(), name='news_update'),
    path('news/<int:pk>/delete', PostDelete.as_view(), name='news_delete'),
    path('article/create', ArticleCreate.as_view(), name='article_create'),
    path('article/<int:pk>/update', ArticleUpdate.as_view(), name='article_update'),
    path('article/<int:pk>/delete', ArticleDelete.as_view(), name='article_delete'),
    path('news/login', LoginRequired.as_view(), name='login'),
    path('news/logout', LogoutView.as_view(), name='logout'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),

]
