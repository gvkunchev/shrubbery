from django import forms

from .models import FinalScheduleSlot


class FinalScheduleSlotForm(forms.ModelForm):

    class Meta:
        model = FinalScheduleSlot
        fields = ('start', 'end')

    def clean(self):
        """Clean up before save, ensuring the custom model is correct."""
        cleaned_data = super().clean()
        start = cleaned_data.get("start")
        end = cleaned_data.get("end")
        if start >= end:
            self.add_error("end", 'Началото трябва да е преди края.')
