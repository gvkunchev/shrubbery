from django import forms

from .models import (ChallengeSolution, ChallengeSolutionComment,
                     ChallengeSolutionInlineComment, ChallengeSolutionTeacherPoints)


class ChallengeSolutionForm(forms.ModelForm):

    class Meta:
        model = ChallengeSolution
        fields = ('challenge', 'author', 'content')


class ChallengeSolutionCommentForm(forms.ModelForm):

    class Meta:
        model = ChallengeSolutionComment
        fields = ('solution', 'content', 'author')


class ChallengeSolutionTeacherPointsForm(forms.ModelForm):

    class Meta:
        model = ChallengeSolutionTeacherPoints
        fields = ('solution', 'points')


class ChallengeSolutionInlineCommentForm(forms.ModelForm):

    class Meta:
        model = ChallengeSolutionInlineComment
        fields = ('solution', 'content', 'author', 'line')
