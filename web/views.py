from django.contrib.auth.decorators import login_required
from django.db.models import OuterRef, Subquery
from django.utils.decorators import method_decorator
from django.views import generic
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from .forms import ActivityScoreForm
from .models import (
    Activity,
    ActivityScore,
    Candidate,
    Mentor,
    Team
)


@method_decorator(login_required, name='dispatch')
class CandidateListView(generic.ListView):
    context_object_name = 'candidate_list'
    template_name = 'candidate_list.html'

    def get_queryset(self):
        queryset = Candidate.objects.add_average_score()

        if self.request.user.is_mentor:
            return queryset.filter(team__mentors__user=self.request.user)

        if self.request.user.is_admin:
            return queryset


@method_decorator(login_required, name='dispatch')
class CandidateDetailView(generic.DetailView):
    queryset = Candidate.objects.add_average_score()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team'] = Team.objects.add_average_score().filter(candidate=self.object).first()
        context['title'] = self.object.user.get_full_name
        return context


@method_decorator(login_required, name='dispatch')
class TeamListView(generic.ListView):
    context_object_name = 'team_list'
    template_name = 'team_list.html'

    def get_queryset(self):
        queryset = Team.objects.add_average_score()
        if self.request.user.is_mentor:
            return queryset.filter(mentors__user=self.request.user)

        if self.request.user.is_admin:
            return queryset


@method_decorator(login_required, name='dispatch')
class TeamDetailView(generic.DetailView):
    queryset = Team.objects.add_average_score()


@method_decorator(login_required, name='dispatch')
class ActivityListView(generic.ListView):
    context_object_name = 'activity_list'
    template_name = 'activity_list.html'

    def get_queryset(self):
        queryset = Activity.objects.add_average_score()
        if self.request.user.is_mentor:
            activityscore_qs = ActivityScore.objects \
                .filter(activity=OuterRef('id'), mentor__user=self.request.user)
            return queryset.annotate(mentor_score=Subquery(activityscore_qs.values('score')[:1]))

        if self.request.user.is_admin:
            return queryset


# TODO: Make this cleaner
@method_decorator(login_required, name='dispatch')
class ActivityFormView(generic.edit.FormView):
    template_name = 'web/activity_form.html'
    form_class = ActivityScoreForm
    success_url = reverse_lazy('activities')

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        activity = context['activity']
        activityscore = activity.activityscore_set.filter(mentor__user=self.request.user).first()
        if activityscore:
            context['form'] = self.form_class(instance=activityscore)
        return self.render_to_response(context)

    def form_valid(self, form):
        activity = Activity.objects.get(pk=self.kwargs['pk'])
        mentor = Mentor.objects.get(user=self.request.user)
        score = self.request.POST['score']
        activityscore = ActivityScore.objects.filter(activity=activity, mentor=mentor).first()
        if activityscore:
            activityscore.score = score
        else:
            activityscore = ActivityScore(
                activity=activity,
                mentor=mentor,
                score=score
            )
        activityscore.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activity'] = get_object_or_404(Activity, pk=kwargs['pk'])
        return context
