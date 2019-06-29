from django.views import generic

from .models import (
    Candidate
)


class CandidateListView(generic.ListView):
    model = Candidate


class CandidateDetailView(generic.DetailView):
    model = Candidate
