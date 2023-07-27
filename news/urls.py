from django.urls import path
from news.views import PostsList, PostsDetail

urlpatterns = [
    path('', PostsList.as_view()),
    path('<int:pk>', PostsDetail.as_view()),
]