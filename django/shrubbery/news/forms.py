from django import forms

from .models import NewsArticle


class AddNewsArticleForm(forms.ModelForm):

    class Meta:
        model = NewsArticle
        fields = ('title', 'content', 'author')
        error_messages = {
            'title': {
                'required': "Това поле е задължително",
            },
            'content': {
                'required': "Това поле е задължително",
            }
        }
