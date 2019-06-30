from django.core.management.base import BaseCommand

from web.models import User, Team
from seed.factory import (
    ActivityFactory,
    ActivityScoreFactory,
    AdminFactory,
    CandidateFactory,
    MentorFactory,
    TeamFactory,
    UserFactory,
)


class Command(BaseCommand):
    help = 'Seed the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force the seeder to run, resulting in all data being lost.'
        )

    def handle(self, *args, **options):
        if not options['force']:
            print('WARNING: Running this command will clear all data. Run with `--force` to continue')
            return

        User.objects.all().delete()
        Team.objects.all().delete()

        # randomly chosen values
        AdminFactory()
        TeamFactory.create_batch(6)
        UserFactory.reset_sequence(0)
        MentorFactory.create_batch(3)
        UserFactory.reset_sequence(0)
        CandidateFactory.create_batch(18)
        ActivityFactory.create_batch(50)
        for _ in range(100):
            ActivityScoreFactory()
