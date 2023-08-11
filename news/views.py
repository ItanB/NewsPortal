from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from .forms import PostForm
from .models import Post
from .filters import PostFilter


@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='author')
    if not request.user.groups.filter(name='author').exists():
        author_group.user_set.add(user)
    return redirect('/')


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


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'
    permission_required = 'news.add_post'
    success_url = reverse_lazy('news_search')


class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'
    permission_required = 'news.change_post'
    success_url = reverse_lazy('news_search')


class LoginRequired(TemplateView):
    template_name = 'base.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
    #     return context


class Logout(TemplateView):
    template_name = 'login.html'


class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'news_delete.html'
    permission_required = 'news.delete_post'
    success_url = reverse_lazy('news_search')


class ArticleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'article_create.html'
    permission_required = 'news.add_post'
    success_url = reverse_lazy('news_search')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'AR'
        return super().form_valid(form)


class ArticleUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'article_create.html'
    permission_required = 'news.change_post'
    success_url = reverse_lazy('news_search')


class ArticleDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'news_delete.html'
    permission_required = 'news.delete_post'
    success_url = reverse_lazy('news_search')
