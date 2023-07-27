from django.shortcuts import render

from django.views.generic import ListView, DetailView
from .models import Post


class PostsList(ListView):
    model = Post
    ordering = '-id'
    template_name = 'news.html'
    context_object_name = 'posts'


class PostsDetail(DetailView):
    model = Post
    template_name = 'postsdetails.html'
    context_object_name = 'post'
