import csv

import pycountry
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from artifacts.models import Artifact, ArtifactType, ArtifactMaterial


class Command(BaseCommand):
    help = "Import artifacts from csv."

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)

    def handle(self, filename, *args, **options):
        with open(f'csv_files/{filename}.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                item_no = row['item_no']
                title_he = row['title_he']
                title_en = row['title_en']
                slug_field = row['slug']
                slug = slug_field if slug_field else slugify(title_en, allow_unicode=True)

                if Artifact.objects.filter(slug=slug).exists():
                    continue

                country = row['country']
                city_he = row['city_he']
                city_en = row['city_en']
                story_he = row['story_he']
                story_en = row['story_en']
                year_from = row['year_from']
                year_to = row['year_to']
                a_type = row['type']
                material = row['material']
                donor_he = row['donor_he']
                donor_en = row['donor_en']
                credit_he = row['credit_he']
                credit_en = row['credit_en']

                if country:
                    if country.lower() == 'iran':
                        c = 'IR'
                    elif country.lower() == 'holland':
                        c = 'NL'
                    else:
                        c = pycountry.countries.lookup(country).alpha_2
                else:
                    c = None
                artifact = Artifact()
                artifact.item_no = item_no
                artifact.artifact_type = ArtifactType.objects.get(title_en=a_type)
                artifact.name_en = title_en
                artifact.name_he = title_he
                artifact.slug = slug
                if year_from:
                    artifact.year_from = int("".join([x for x in year_from if x.isdigit()]))
                if year_to:
                    artifact.year_to = int("".join([x for x in year_to if x.isdigit()]))
                artifact.description_he = story_he
                artifact.description_en = story_en
                artifact.origin_city_he = city_he
                artifact.origin_city_en = city_en
                if country:
                    artifact.origin_country = c
                artifact.donor_name_he = donor_he
                artifact.donor_name_en = donor_en
                artifact.display_donor_name = True
                artifact.credit_he = credit_he
                artifact.credit_en = credit_en
                artifact.save()

                if material:
                    materials = material.split(',')
                    all_materials = ArtifactMaterial.objects.filter(title_en__in=materials)
                    artifact.artifact_materials.add(*all_materials)

        self.stdout.write(self.style.SUCCESS('Successfully create all artifacts'))
