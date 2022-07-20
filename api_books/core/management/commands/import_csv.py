import csv

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist

from api_books.core.models import Author


class Command(BaseCommand):

    help = 'import authors.csv to db'

    @staticmethod
    def _clean_name(name):
        return name.strip()

    def add_arguments(self, parser):
        parser.add_argument('file_name', type=str)

    def handle(self, *args, **options):

        file_name = options['file_name']

        try:
            with open(file_name) as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                # header
                next(spamreader)
                authors = []
                count = 0
                for row in spamreader:
                    name = Command._clean_name(row[0])
                    try:
                        Author.objects.get(name=name)
                    except ObjectDoesNotExist:
                        count += 1
                        authors.append(Author(name=name))

                Author.objects.bulk_create(authors)

            self.stdout.write(self.style.SUCCESS(f'{count} registros importados do Arquivo {file_name}'))

        except FileNotFoundError:
            raise CommandError(f'File {file_name} not found')
