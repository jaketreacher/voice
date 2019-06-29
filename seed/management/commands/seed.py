from django.core.management.base import BaseCommand

from web.models import User, Team, Admin
from seed.factory import (
    ActivityFactory,
    ActivityScoreFactory,
    AdminFactory,
    CandidateFactory,
    MentorFactory,
    TeamFactory
)


class Command(BaseCommand):
    help = 'Seed the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clean',
            action='store_true',
            help='Clear all models from the database before creating a new batch.'
        )

        parser.add_argument(
            '--none',
            action='store_true',
            help='Run the seeder without actually seeding anything.'
        )

    def handle(self, *args, **options):
        if options['clean']:
            User.objects.all().delete()
            Team.objects.all().delete()

        if options['none']:
            return self.test()

        if not Admin.objects.count():
            admin = AdminFactory(user__username='admin')
            admin.user.set_password('password')
            admin.user.save()

        # randomly chosen values
        TeamFactory.create_batch(6)
        MentorFactory.create_batch(3)
        CandidateFactory.create_batch(18)
        ActivityFactory.create_batch(50)
        for _ in range(100):
            ActivityScoreFactory()
