import csv

import os
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.core.management.base import BaseCommand

from artifacts.models import Artifact, ArtifactImage


class Command(BaseCommand):
    help = "Import artifacts images from csv."

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)

    def handle(self, filename, *args, **options):
        with open(f'csv_files/{filename}.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                item_no = row['item_no']

                if not item_no:
                    continue

                filename = row['filename']

                if not filename:
                    continue

                title_he = row['title_he']
                title_en = row['title_en']
                where_he = row['where_he']
                where_en = row['where_en']
                when_he = row['when_he']
                when_en = row['when_en']
                name_he = row['name_he']
                name_en = row['name_en']
                try:
                    artifact = Artifact.objects.get(item_no=item_no)
                except Artifact.DoesNotExist:
                    continue

                img = ArtifactImage()
                img.artifact = artifact
                img.description_he = title_he
                img.description_en = title_en
                img.credit_he = name_he
                img.credit_en = name_en
                img.year_era_he = when_he
                img.year_era_en = when_en
                img.location_he = where_he
                img.location_en = where_en
                fn = os.path.join(settings.BASE_DIR, f'artifact_images/{filename}.jpg')
                img.image = UploadedFile(open(fn, "br"))
                img.save()

        self.stdout.write(self.style.SUCCESS('Successfully create all artifacts'))
