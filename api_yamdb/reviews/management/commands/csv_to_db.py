from django.core.management.base import BaseCommand, CommandError
import csv
from reviews.models import Genre, Title, Category, Review, GenreTitle, User


MODELS_FILES = {
        Genre: 'static/data/genre.csv',
        Category: 'static/data/category.csv',
        Title: 'static/data/titles.csv',
        # Review: 'static/data/review.csv',
        GenreTitle: 'static/data/genre_title.csv',
        User: 'static/data/users.csv'
    }


class Command(BaseCommand):
    help = 'load data from csv'

    def handle(self, *args, **options):
        for model, dir_to_file in MODELS_FILES.items():
            with open(dir_to_file, encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=',')
                for row in csv_reader:
                    model.objects.get_or_create(**row)
