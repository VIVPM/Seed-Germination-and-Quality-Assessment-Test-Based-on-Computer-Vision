# Generated by Django 4.2 on 2023-05-13 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seed', '0030_remove_season_from_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Variety',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('yield_per_acre', models.CharField(max_length=50)),
                ('maturity_duration', models.DateField()),
                ('description', models.TextField()),
                ('variety_image', models.ImageField(blank=True, null=True, upload_to='images/')),
            ],
        ),
    ]