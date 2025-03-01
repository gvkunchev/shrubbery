from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm

from .models import Student, Teacher, User


class PasswordSetForm(PasswordChangeForm):

    class Meta:
        model = User
        fields = ('new_password1', 'new_password1')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].required = False


class EditUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('github', 'image', 'dark_theme')


class EmailSettingsForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email_notification_news', 'email_notification_forum',
                  'email_notification_homework', 'email_notification_challenge',
                  'email_notification_solution_comments')


class AddStudentForm(UserCreationForm):

    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'fn')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False


class RegisterStudent(forms.ModelForm):

    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'fn', 'email')


class EditStudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'fn')


class AddTeacherForm(UserCreationForm):

    class Meta:
        model = Teacher
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False


class EditTeacherForm(forms.ModelForm):

    class Meta:
        model = Teacher
        fields = ('first_name', 'last_name')
