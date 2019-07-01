from django import forms

from .models import Activity, ActivityScore


class ActivityScoreForm(forms.ModelForm):
    mentor_id = forms.IntegerField(widget=forms.HiddenInput(), disabled=True)
    score = forms.IntegerField(max_value=100, min_value=0)

    class Meta:
        model = Activity
        fields = []

    def save(self, commit=True):
        activity = self.instance
        mentor_id = self.cleaned_data['mentor_id']
        score = self.cleaned_data['score']

        activityscore = activity.activityscore_set.filter(mentor_id=mentor_id).first()
        if activityscore:
            activityscore.score = score
            activityscore.save()
        else:
            ActivityScore.objects.create(activity=activity,mentor_id=mentor_id,score=score)

        return activity
