from django import forms

from .models import Homework, HomeworkComment


class HomeworkForm(forms.ModelForm):

    class Meta:
        model = Homework
        fields = ('title', 'content', 'deadline', 'author',
                  'points', 'sanity_test', 'full_test',
                  'hidden', 'verified')


class HomeworkCommentForm(forms.ModelForm):

    class Meta:
        model = HomeworkComment
        fields = ('homework', 'content', 'author')
