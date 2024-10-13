from django.core.management.base import BaseCommand
from farm_management.models import RoverData, Parcel, Activity, ReferencePoint
from django.contrib.gis.geos import Point, Polygon
from datetime import timedelta

class Command(BaseCommand):
    help = 'Popula la base de datos con datos iniciales'

    def handle(self, *args, **kwargs):

        parcel1 = Parcel.objects.create(
            name='Parcel 1',
            boundary=Polygon(((37.69428, -122.44586), (37.69455, -122.44586), (37.69455, -122.44559), (37.69428, -122.44559),(37.69428, -122.44586)))  # Polígono de ejemplo
        )
        # Crear Actividades
        activity1 = Activity.objects.create(
            name='Revisión de Cultivos',
            is_complete=False,
            time_required=timedelta(seconds=20)  
        )
        activity2 = Activity.objects.create(
            name='Revisión de Riego',
            is_complete=False,
            time_required=timedelta(seconds=10)  
        )
        # Crear Puntos de Referencia
        reference_point1 = ReferencePoint.objects.create(
            parcel=parcel1,
            location=Point(37.694415, -122.44586),  # Ubicación del punto de referencia
            activity=activity1
        )
        reference_point2 = ReferencePoint.objects.create(
            parcel=parcel1,
            location=Point(37.69455, -122.445725),  # Ubicación del punto de referencia
            activity=activity2
        )
        reference_point3 = ReferencePoint.objects.create(
            parcel=parcel1,
            location=Point(37.694415, -122.44559),  # Ubicación del punto de referencia
            activity=activity1
        )
        reference_point4 = ReferencePoint.objects.create(
            parcel=parcel1,
            location=Point(37.69428, -122.445725),  # Ubicación del punto de referencia
            activity=activity2
        )

        self.stdout.write(self.style.SUCCESS('Datos iniciales creados exitosamente.'))