from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='web/home.html'), name='home'),
    path('accounts/login/rediect/', views.login_redirect, name='login-redirect'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('candidates/', login_required(views.CandidateListView.as_view()), name='candidates'),
    path('candidate/<int:pk>', login_required(views.CandidateDetailView.as_view()), name='candidate-detail'),

    path('teams/', login_required(views.TeamListView.as_view()), name='teams'),
    path('team/<int:pk>', login_required(views.TeamDetailView.as_view()), name='team-detail'),

    path('activities/', login_required(views.ActivityListView.as_view()), name='activities'),

    path('activity/<int:pk>/score', login_required(views.ActivityScoreFormView.as_view()), name='activity-form'),
]
