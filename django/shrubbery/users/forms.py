from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Student, User


class AddStudentForm(UserCreationForm):

    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'fn')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False


class EditStudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'fn')


class EditUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'github', 'image', 'dark_theme')
