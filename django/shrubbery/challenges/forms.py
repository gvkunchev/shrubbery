from django import forms

from .models import Challenge, ChallengeComment


class ChallengeForm(forms.ModelForm):

    class Meta:
        model = Challenge
        fields = ('title', 'content', 'deadline', 'author',
                  'points', 'sanity_test', 'full_test',
                  'custom_module_name', 'custom_module_content',
                  'hidden', 'verified')

    def clean(self):
        """Clean up before save, ensuring the custom model is correct."""
        cleaned_data = super().clean()
        module_name = cleaned_data.get("custom_module_name")
        module_content = cleaned_data.get("custom_module_content")
        if module_name in ('solution', 'test'):
            self.add_error("custom_module_name", 'Това име е запазено.')
        if module_name and not module_content:
            self.add_error("custom_module_content", 'Това поле е задължително, ако е дефинирано име на модула.')
        if module_content and not module_name:
            self.add_error("custom_module_name", 'Това поле е задължително, ако е дефинирано съдържание на модула.')


class ChallengeCommentForm(forms.ModelForm):

    class Meta:
        model = ChallengeComment
        fields = ('challenge', 'content', 'author', 'parent')
