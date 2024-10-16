# Generated by Django 5.0.6 on 2024-10-14 12:59

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farm_management', '0005_delete_roverdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoverData',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('orientation', models.FloatField()),
                ('status', models.CharField(choices=[('active', 'Activo'), ('inactive', 'Inactivo'), ('in_mission', 'En Misión')], max_length=20)),
                ('speed', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
