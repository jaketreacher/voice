from django.db import models
from django.db.models import Avg
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    UserType = {
        'admin': 1,
        'mentor': 2,
        'candidate': 3
    }
    type = models.SmallIntegerField(choices=[(val, key) for key, val in UserType.items()])

    def is_mentor(self):
        return self.type == self.UserType['mentor']

    def is_candidate(self):
        return self.type == self.UserType['candidate']

    def is_admin(self):
        return self.type == self.UserType['admin']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_candidate():
            Candidate.objects.create(user=self)
        elif self.is_mentor():
            Mentor.objects.create(user=self)


class Candidate(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    team = models.ForeignKey('Team', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return str(self.user)


class Mentor(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)


class Team(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<{}: {} ({})>' % (self.__class__.__name__, self.name, self.pk)


class MentorTeam(models.Model):
    team = models.ForeignKey('Team', on_delete=models.SET_NULL, blank=True, null=True)
    mentor = models.ForeignKey('Mentor', on_delete=models.SET_NULL, blank=True, null=True)


class Activity(models.Model):
    candidate = models.ForeignKey('Candidate', on_delete=models.CASCADE)
    song_name = models.CharField(max_length=128)
    performance_date = models.DateField()

    @property
    def average_score(self):
        return self.activityscore_set.aggregate(Avg('score'))['score__avg']


class ActivityScore(models.Model):
    mentor = models.ForeignKey('Mentor', on_delete=models.CASCADE)
    activity = models.ForeignKey('Activity', on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])
