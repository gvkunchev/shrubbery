from django import forms

from .models import (HomeworkSolution, HomeworkSolutionComment,
                     HomeworkSolutionInlineComment, HomeworkSolutionTeacherPoints)


class HomeworkSolutionForm(forms.ModelForm):

    class Meta:
        model = HomeworkSolution
        fields = ('homework', 'author', 'content')


class HomeworkSolutionCommentForm(forms.ModelForm):

    class Meta:
        model = HomeworkSolutionComment
        fields = ('solution', 'content', 'author')


class HomeworkSolutionTeacherPointsForm(forms.ModelForm):

    class Meta:
        model = HomeworkSolutionTeacherPoints
        fields = ('solution', 'points')


class HomeworkSolutionInlineCommentForm(forms.ModelForm):

    class Meta:
        model = HomeworkSolutionInlineComment
        fields = ('solution', 'content', 'author', 'line')
