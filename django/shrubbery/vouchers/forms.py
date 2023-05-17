from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm

from .models import Voucher


class VoucherForm(forms.ModelForm):

    class Meta:
        model = Voucher
        fields = ('token', 'points')
