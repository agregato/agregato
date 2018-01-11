from django.core.management.base import BaseCommand

from allegro.tasks import delete_old


class Command(BaseCommand):
    help = 'Checks all wtches for update'

    def handle(self, *args, **options):
        delete_old()
