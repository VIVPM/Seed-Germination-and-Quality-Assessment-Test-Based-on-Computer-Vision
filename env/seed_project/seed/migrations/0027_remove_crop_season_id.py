# Generated by Django 4.2 on 2023-05-13 09:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seed', '0026_remove_season_from_date_remove_season_to_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='crop',
            name='season_id',
        ),
    ]
