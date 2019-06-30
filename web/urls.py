from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='web/home.html'), name='home'),

    path('candidates/', login_required(views.CandidateListView.as_view()), name='candidates'),
    path('candidate/<int:pk>', login_required(views.CandidateDetailView.as_view()), name='candidate-detail'),

    path('teams/', login_required(views.TeamListView.as_view()), name='teams'),
    path('team/<int:pk>', login_required(views.TeamDetailView.as_view()), name='team-detail'),

    path('activities/', login_required(views.ActivityListView.as_view()), name='activities'),

    path('activity/<int:pk>', login_required(views.ActivityFormView.as_view()), name='activity-form'),

    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/login/rediect/', views.login_redirect, name='login-redirect'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]
