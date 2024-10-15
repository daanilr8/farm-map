from farm_management.models import Activity,ReferencePoint,Parcel,RoverData
from django.core.management.base import BaseCommand
from datetime import timedelta
from django.contrib.gis.geos import Point


class Command(BaseCommand):
    help = 'Crea una nueva actividad en la base de datos'

    def handle(self, *args, **kwargs):

        roverData = RoverData.objects.all()

        for rover in roverData:
            rover.delete()

        self.stdout.write(self.style.SUCCESS(f'Actividad creada exitosamente.'))