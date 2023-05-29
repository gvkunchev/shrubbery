from django import forms

from .models import Challenge, ChallengeComment


class ChallengeForm(forms.ModelForm):

    class Meta:
        model = Challenge
        fields = ('title', 'content', 'deadline',
                  'points', 'sanity_test', 'full_test',
                  'hidden', 'verified')


class ChallengeCommentForm(forms.ModelForm):

    class Meta:
        model = ChallengeComment
        fields = ('challenge', 'content', 'author')
