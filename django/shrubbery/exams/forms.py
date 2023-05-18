from django import forms

from .models import Exam, ExamResult


class ExamForm(forms.ModelForm):

    class Meta:
        model = Exam
        fields = ('date', 'title')


class ExamResultForm(forms.ModelForm):

    class Meta:
        model = ExamResult
        fields = ('owner', 'exam', 'points')
