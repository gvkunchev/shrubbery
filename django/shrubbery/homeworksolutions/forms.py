from django import forms

from .models import HomeworkSolution


class HomeworkSolutionForm(forms.ModelForm):

    class Meta:
        model = HomeworkSolution
        fields = ('homework', 'author', 'content')
