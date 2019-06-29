from django.contrib import admin
from .models import (
    Activity,
    ActivityScore,
    Admin,
    Candidate,
    Mentor,
    Team,
)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    pass


@admin.register(ActivityScore)
class ActivityScoreAdmin(admin.ModelAdmin):
    list_display = ['song_name', 'score', 'candidate_name', 'mentor_name']
    search_fields = [
        'activity__song_name',
        'activity__candidate__user__first_name',
        'activity__candidate__user__last_name',
        'activity__mentor__user__first_name',
        'activity__mentor__user__last_name',
    ]
    ordering = ['activity__song_name']

    def song_name(self, obj):
        return obj.activity.song_name
    song_name.admin_order_field = 'activity__song_name'

    def candidate_name(self, obj):
        return obj.activity.candidate.user.get_full_name()
    candidate_name.admin_order_field = 'activity__candidate__user__last_name'

    def mentor_name(self, obj):
        return obj.mentor.user.get_full_name()
    mentor_name.admin_order_field = 'mentor__user__last_name'


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    pass


class ActivityInline(admin.StackedInline):
    model = Activity


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    ordering = ['user__last_name']
    search_fields = [
        'user__first_name',
        'user__last_name'
    ]

    inlines = [ActivityInline]


@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    pass


class CandidateInline(admin.StackedInline):
    model = Candidate


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    inlines = [CandidateInline]
