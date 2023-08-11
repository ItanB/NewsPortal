from django.db import models
from django.contrib.auth.models import User
import django.utils.timezone
from django.db.models import Sum
from django.db.models.functions import Coalesce
from typing import List, Tuple
from django.core.validators import MinValueValidator
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='basic')
        basic_group.user_set.add(user)
        return user

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    def update_rating(self):
        author_posts_rating = Post.objects.filter(post_author_id=self.pk).aggregate(
            post_rating_sum=Coalesce(Sum('rating') * 3, 0))
        author_comment_rating = Comment.objects.filter(user_id=self.user).aggregate(
            comments_rating_sum=Coalesce(Sum('rating'), 0))
        author_post_comment_rating = Comment.objects.filter(post__author__name=self.user).aggregate(
            comments_rating_sum=Coalesce(Sum('rating'), 0))
        self.rating_autor = author_posts_rating['rating_sum'] + author_comment_rating['rating_sum'] + \
                            author_post_comment_rating['rating_sum']
        self.save()


class Category(models.Model):
    category = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.category.title()


class Post(models.Model):
    objects = None
    article = 'AR'
    news = 'NE'
    types = [
        (news, 'Новость'),
        (article, 'Статья')
    ]
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)

    type = models.CharField(max_length=100, choices=types)
    post_time = models.DateTimeField(default=django.utils.timezone.now)
    categories = models.ManyToManyField(Category, through="PostCategory")
    title = models.CharField(max_length=255, null=False)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.title.title()}: {self.text[:20]}'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    objects = None
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(default=django.utils.timezone.now)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.title()}: {self.text[:20]}'

    def like(self):
        self.rating += 1

    def dislike(self):
        self.rating -= 1


class Protected(models.Model):
    pass
