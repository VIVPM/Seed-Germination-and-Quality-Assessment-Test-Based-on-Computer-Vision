# Generated by Django 4.2 on 2023-05-12 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seed', '0024_alter_crop_maturity_date_alter_crop_sowing_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='season',
            name='from_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='season',
            name='to_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
