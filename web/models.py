from django.db import models
from django.db.models import Avg, Count, Q
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import AbstractUser


class UserQuerySet(models.QuerySet):
    def candidate_only(self):
        return self.filter(is_candidate=True)

    def mentor_only(self):
        return self.filter(is_mentor=True)

    def admin_only(self):
        return self.filter(is_admin=True)


class CandidateManager(models.Manager):
    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db).mentor_only()


class MentorManager(models.Manager):
    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db).candidate_only()


class AdminManager(models.Manager):
    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db).admin_only()


class User(AbstractUser):
    is_candidate = models.BooleanField(default=False)
    is_mentor = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=~(Q(is_admin=True) & Q(is_candidate=True)),
                name='admin_candidate_mutually_exclusive'
            ),
            models.CheckConstraint(
                check=~(Q(is_admin=True) & Q(is_mentor=True)),
                name='admin_mentor_mutually_exclusive'
            ),
            models.CheckConstraint(
                check=~(Q(is_candidate=True) & Q(is_mentor=True)),
                name='candidate_mentor_mutually_exclusive'
            ),
        ]

    objects = models.Manager()
    candidates = CandidateManager()
    mentors = MentorManager()
    admin = AdminSet.as_manager()


class Candidate(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    team = models.ForeignKey('Team', on_delete=models.SET_NULL, blank=True, null=True)

    @property
    def average_score(self):
        return self.activity_set.aggregate(avg=Avg('activityscore__score'))['avg']

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

    @property
    def average_score(self):
        return self.candidate_set.aggregate(avg=Avg('activity__activityscore__score'))['avg']

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<%s: %s (%d)>' % (self.__class__.__name__, self.name, self.pk)


class Activity(models.Model):
    candidate = models.ForeignKey('Candidate', on_delete=models.CASCADE)
    song_name = models.CharField(max_length=128)
    performance_date = models.DateField()

    class Meta:
        ordering = ['-performance_date']

    @property
    def average_score(self):
        return self.activityscore_set.aggregate(avg=Avg('score'))['avg']

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
