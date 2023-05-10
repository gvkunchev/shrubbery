from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Student


class AddStudentForm(UserCreationForm):

    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'fn')
        error_messages = {
            'first_name': {
                'required': "Това поле е задължително",
            },
            'last_name': {
                'required': "Това поле е задължително",
            },
            'fn': {
                'required': "Това поле е задължително",
                'unique': "Вече има студент с този ФН",
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False


class EditStudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'fn')
        error_messages = {
            'first_name': {
                'required': "Това поле е задължително",
            },
            'last_name': {
                'required': "Това поле е задължително",
            },
            'fn': {
                'required': "Това поле е задължително",
                'unique': "Вече има друг студент с този ФН",
            },
        }
