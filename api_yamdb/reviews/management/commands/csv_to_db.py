import csv

from django.core.management.base import BaseCommand

from reviews.models import (Category, Comment, Genre, GenreTitle, Review,
                            Title, User)

MODELS_FILES = {
    User: 'static/data/users.csv',
    Genre: 'static/data/genre.csv',
    Category: 'static/data/category.csv',
    Title: 'static/data/titles.csv',
    Review: 'static/data/review.csv',
    GenreTitle: 'static/data/genre_title.csv',
    Comment: 'static/data/comments.csv'
}


class Command(BaseCommand):
    help = 'load data from csv'

    def handle(self, *args, **options):
        for model, dir_to_file in MODELS_FILES.items():
            with open(dir_to_file, encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=',')
                for row in csv_reader:
                    model.objects.get_or_create(**row)
