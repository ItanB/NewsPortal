import django_filters.widgets
from django.forms import SelectDateWidget
from django_filters import FilterSet, CharFilter, DateFilter
from django_filters.widgets import DateRangeWidget

from .models import Post


class PostFilter(FilterSet):
    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Заголовок'
    )
    author = CharFilter(
        field_name='post_author__user__username',
        lookup_expr='icontains',
        label='Автор'
    )
    post_time = DateFilter(
        widget=SelectDateWidget(),

        lookup_expr='gt',
        label='За период не раннее'
    )

    class Meta:
        model = Post
        fields = {'title'}