from django import forms

from .models import Forum, ForumComment


class ForumForm(forms.ModelForm):

    class Meta:
        model = Forum
        fields = ('author', 'content', 'title')


class ForumCommentForm(forms.ModelForm):

    class Meta:
        model = ForumComment
        fields = ('forum', 'content', 'author')
