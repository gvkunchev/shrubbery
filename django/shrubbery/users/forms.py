from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm

from .models import Student, User


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


class EditUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'github', 'image')
        error_messages = {
            'first_name': {
                'required': "Това поле е задължително",
            },
            'last_name': {
                'required': "Това поле е задължително",
            }
        }


class PasswordChangeTranslatedForm(PasswordChangeForm):
    
    error_messages = {
        'password_incorrect': 'Грешна парола',
        'password_mismatch': 'Паролите не съвпадат'
    }
