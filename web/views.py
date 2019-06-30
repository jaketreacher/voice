from django.contrib.auth.decorators import login_required
from django.db.models import OuterRef, Subquery
from django.utils.decorators import method_decorator
from django.views import generic

from .models import (
    Candidate,
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

