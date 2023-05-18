from django import forms

from .models import NewsArticle


class NewsArticleForm(forms.ModelForm):

    class Meta:
        model = NewsArticle
        fields = ('title', 'content', 'author')
