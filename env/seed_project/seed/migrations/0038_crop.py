# Generated by Django 4.2 on 2023-05-14 08:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seed', '0037_alter_season_from_date_alter_season_to_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Crop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('plant_type', models.CharField(max_length=50)),
                ('soil_type', models.CharField(max_length=50)),
                ('cultivation_type', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('crop_image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('area', models.CharField(max_length=50)),
                ('season_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='seed.season')),
                ('variety_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='seed.variety')),
            ],
        ),
    ]