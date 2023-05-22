from django import forms

from .models import HomeworkSolution, HomeworkSolutionComment


class HomeworkSolutionForm(forms.ModelForm):

    class Meta:
        model = HomeworkSolution
        fields = ('homework', 'author', 'content')


class HomeworkSolutionCommentForm(forms.ModelForm):

    class Meta:
        model = HomeworkSolutionComment
        fields = ('solution', 'content', 'author')
