from django import forms

from .models import ActivityScore


class ActivityScoreForm(forms.ModelForm):

    class Meta:
        model = ActivityScore
        fields = ('score',)
