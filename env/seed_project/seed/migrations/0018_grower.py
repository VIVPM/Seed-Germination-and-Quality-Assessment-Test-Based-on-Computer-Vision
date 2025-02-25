# Generated by Django 4.2 on 2023-05-11 12:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seed', '0017_city_country_state'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aadhar_number', models.CharField(max_length=12)),
                ('pan_number', models.CharField(max_length=10)),
                ('mobile_number', models.CharField(max_length=10)),
                ('address', models.TextField()),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('city_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='seed.city')),
                ('country_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='seed.country')),
                ('state_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='seed.state')),
            ],
        ),
    ]
