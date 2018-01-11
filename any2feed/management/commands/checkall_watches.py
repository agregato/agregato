from django.core.management.base import BaseCommand

from any2feed.tasks import check_watches


class Command(BaseCommand):
    help = 'Checks all wtches for update'

    def handle(self, *args, **options):
        check_watches()
