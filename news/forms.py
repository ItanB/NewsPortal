from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            'title',
            'post_author',
            'categories',
            'text',
        ]

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("title")
        content = cleaned_data.get("text")

        if name == content:
            raise ValidationError(
                "добавьте текст новости, она не может совпадать с заголовком"
            )

        return cleaned_data
