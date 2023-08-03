from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import PostForm
from .models import Post
from .filters import PostFilter


class PostsList(ListView):
    model = Post
    ordering = '-id'
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostsDetail(DetailView):
    model = Post
    template_name = 'postsdetails.html'
    context_object_name = 'post'


class SearchPostList(ListView):
    model = Post
    ordering = '-id'
    template_name = 'news_search.html'
    context_object_name = 'news_search'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'
    success_url = reverse_lazy('news_search')


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'
    success_url = reverse_lazy('news_search')


class PostDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_search')


class ArticleCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'article_create.html'
    success_url = reverse_lazy('news_search')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'AR'
        return super().form_valid(form)


class ArticleUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'article_create.html'
    success_url = reverse_lazy('news_search')


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_search')
