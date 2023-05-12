from django import forms

from .models import NewsArticle


class AddNewsArticleForm(forms.ModelForm):

    class Meta:
        model = NewsArticle
        fields = ('title', 'content', 'author')
