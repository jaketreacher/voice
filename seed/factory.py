import factory
from web.models import (
    Activity,
    ActivityScore,
    Admin,
    Candidate,
    Mentor,
    Team,
    User,
)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'user%d' % n)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')


class CandidateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Candidate

    user = factory.SubFactory(UserFactory)
    team = factory.Faker('random_element', elements=Team.objects.all())


class MentorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Mentor

    user = factory.SubFactory(UserFactory)

    @factory.post_generation
    def teams(self, create, extracted, **kwargs):
        if extracted:
            for team in extracted:
                self.teams.add(team)
        else:
            self.teams.set(factory.Faker('random_sample', elements=list(Team.objects.all())).generate())


class AdminFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Admin

    user = factory.SubFactory(UserFactory, is_staff=True, is_superuser=True)


class TeamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Team

    name = factory.Faker('sentence', nb_words=3)


class ActivityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Activity

    candidate = factory.Faker('random_element', elements=Candidate.objects.all())
    song_name = factory.Faker('sentence', nb_words=3)
    performance_date = factory.Faker('past_date')


# TODO: Fix this breaking when reaching limit
class ActivityScoreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ActivityScore

    mentor = factory.Faker('random_element', elements=Mentor.mentors_missing_scores())
    score = factory.Faker('pyint', min=0, max=100)

    @factory.lazy_attribute
    def activity(self):
        elements = Activity.objects.exclude(activityscore__mentor=self.mentor)
        return factory.Faker('random_element', elements=elements).generate()
