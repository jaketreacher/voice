from django.db import models
from django.db.models import Avg, Count
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    @property
    def is_mentor(self):
        return Mentor.objects.filter(user__id=self.id).exists()

    @property
    def is_candidate(self):
        return Candidate.objects.filter(user__id=self.id).exists()

    @property
    def is_admin(self):
        return Admin.objects.filter(user__id=self.id).exists()


class Candidate(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    team = models.ForeignKey('Team', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name()


class Mentor(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    @staticmethod
    def mentors_missing_scores():
        return Mentor.objects \
            .annotate(num_activityscore=Count('activityscore')) \
            .filter(num_activityscore__lt=Activity.objects.count())

    def __str__(self):
        return str(self.user)


class Admin(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)


class Team(models.Model):
    name = models.CharField(max_length=128, unique=True)
    mentors = models.ManyToManyField('Mentor', related_name='teams')

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<%s: %s (%d)>' % (self.__class__.__name__, self.name, self.pk)


class Activity(models.Model):
    candidate = models.ForeignKey('Candidate', on_delete=models.CASCADE)
    song_name = models.CharField(max_length=128)
    performance_date = models.DateField()

    @property
    def average_score(self):
        return self.activityscore_set.aggregate(Avg('score'))['score__avg']

    def __str__(self):
        return self.song_name

    def __repr__(self):
        return '<%s: %s (%d)>' % (self.__class__.__name__, self.song_name, self.pk)


class ActivityScore(models.Model):
    mentor = models.ForeignKey('Mentor', on_delete=models.CASCADE)
    activity = models.ForeignKey('Activity', on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])

    class Meta:
        unique_together = ['mentor', 'activity']

    def __str__(self):
        return self.score

    def __repr__(self):
        return '<%s: %s (%d)>' % (self.__class__.__name__, self.score, self.pk)
