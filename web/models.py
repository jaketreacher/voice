from django.db import models
from django.db.models import Avg, Count, OuterRef, Subquery
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


class CandidateSet(models.QuerySet):
    def add_average_score(self):
        subquery = Candidate.objects \
            .values('id').annotate(avg=Avg('activity__activityscore__score')) \
            .filter(id=OuterRef('id'))
        return self.annotate(average_score=Subquery(subquery.values('avg')[:1]))


class Candidate(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    team = models.ForeignKey('Team', on_delete=models.SET_NULL, blank=True, null=True)

    objects = CandidateSet.as_manager()

    def __str__(self):
        return self.user.get_full_name()


class MentorSet(models.QuerySet):
    def add_num_scores(self):
        return self.annotate(num_activityscore=Count('activityscore'))

    def missing_scores(self):
        return self.add_num_missing_scores().filter(num_activityscore__lt=Activity.objects.count())


class Mentor(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    objects = MentorSet.as_manager()

    def __str__(self):
        return str(self.user)


class Admin(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)


class TeamSet(models.QuerySet):
    def add_average_score(self):
        subquery = Team.objects \
            .values('id').annotate(avg=Avg('candidate__activity__activityscore__score')) \
            .filter(id=OuterRef('id'))
        return self.annotate(average_score=Subquery(subquery.values('avg')[:1]))


class Team(models.Model):
    name = models.CharField(max_length=128, unique=True)
    mentors = models.ManyToManyField('Mentor', related_name='teams')

    objects = TeamSet.as_manager()

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<%s: %s (%d)>' % (self.__class__.__name__, self.name, self.pk)


class ActivitySet(models.QuerySet):
    def add_average_score(self):
        subquery = Activity.objects \
            .values('id').annotate(avg=Avg('activityscore__score')) \
            .filter(id=OuterRef('id'))
        return self.annotate(average_score=Subquery(subquery.values('avg')[:1]))


class Activity(models.Model):
    candidate = models.ForeignKey('Candidate', on_delete=models.CASCADE)
    song_name = models.CharField(max_length=128)
    performance_date = models.DateField()

    class Meta:
        ordering = ['-performance_date']

    objects = ActivitySet.as_manager()

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
