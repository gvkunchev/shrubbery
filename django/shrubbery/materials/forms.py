from django import forms

from .models import Material


class EditMaterialForm(forms.ModelForm):

    class Meta:
        model = Material
        fields = ('title', 'content', 'date')
