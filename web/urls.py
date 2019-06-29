from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='web/home.html'), name='home'),
    path('candidates/', views.CandidateListView.as_view(), name='candidates'),
    path('candidate/<int:pk>', views.CandidateDetailView.as_view(), name='candidate-detail'),
]
