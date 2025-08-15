from django.core.management.base import BaseCommand
from apartments.flask import start_fetching_data  # или правильный путь


class Command(BaseCommand):
    help = 'Fetch data from Flask API'

    def handle(self, *args, **options):
        start_fetching_data()
