# Generated by Django 4.2 on 2023-05-15 06:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seed', '0042_grower'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('address', models.TextField()),
                ('pin', models.CharField(max_length=50)),
                ('establishment', models.CharField(max_length=50)),
                ('gst', models.CharField(max_length=50)),
                ('tan', models.TextField()),
                ('website', models.CharField(max_length=50)),
                ('mobile_number', models.CharField(max_length=10)),
                ('email', models.CharField(max_length=50)),
                ('city_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='seed.city')),
                ('country_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='seed.country')),
                ('state_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='seed.state')),
            ],
        ),
    ]