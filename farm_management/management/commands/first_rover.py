from farm_management.models import Activity,ReferencePoint,Parcel,RoverData
from django.core.management.base import BaseCommand
from datetime import timedelta
from django.contrib.gis.geos import Point


class Command(BaseCommand):
    help = 'Crea una nueva posición del Rover 1 en la base de datos'

    def handle(self, *args, **kwargs):
        # Supongamos que quieres actualizar el rover con ID 1
        new_latitude = 37.69428
        new_longitude = -122.44586

        try:
            # Obtener la instancia del rover
            rover = RoverData.objects.get(name='Rover 1')
            # Crear un nuevo objeto Point
            new_location = Point(new_longitude, new_latitude)  # Recuerda que el orden es (longitud, latitud)

            # Modificar la localización
            rover.location = new_location
            rover.save()  # Guardar los cambios en la base de datos

            print('Rover location updated successfully!')
        except RoverData.DoesNotExist:
            print('Rover not found.')

        self.stdout.write(self.style.SUCCESS(f'Actividad creada exitosamente.'))