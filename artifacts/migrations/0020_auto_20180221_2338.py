# Generated by Django 2.0.2 on 2018-02-21 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artifacts', '0019_originarea_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artifact',
            name='year_from',
            field=models.IntegerField(blank=True, null=True, verbose_name='Year from'),
        ),
        migrations.AlterField(
            model_name='artifact',
            name='year_to',
            field=models.IntegerField(blank=True, null=True, verbose_name='Year to'),
        ),
    ]
