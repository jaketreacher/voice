from django.contrib.auth.decorators import login_required
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
        if self.request.user.is_mentor:
            return Candidate.objects.filter(team__mentors__user=self.request.user)

        if self.request.user.is_admin:
            return Candidate.objects.all()


@method_decorator(login_required, name='dispatch')
class CandidateDetailView(generic.DetailView):
    model = Candidate


@method_decorator(login_required, name='dispatch')
class TeamListView(generic.ListView):
    context_object_name = 'team_list'
    template_name = 'team_list.html'

    def get_queryset(self):
        if self.request.user.is_mentor:
            return Team.objects.filter(mentors__user=self.request.user)

        if self.request.user.is_admin:
            return Team.objects.all()


@method_decorator(login_required, name='dispatch')
class TeamDetailView(generic.DetailView):
    model = Team
