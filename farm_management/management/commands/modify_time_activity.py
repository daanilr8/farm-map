from farm_management.models import Activity,ReferencePoint,Parcel
from django.core.management.base import BaseCommand
from datetime import timedelta
from django.contrib.gis.geos import Point

class Command(BaseCommand):
    help = 'Crea una nueva actividad en la base de datos'

    def handle(self, *args, **kwargs):

        # Obtener los puntos de referencia con las actividades relacionadas
        reference_points = ReferencePoint.objects.select_related('activity').all()

        for reference_point in reference_points:
            if reference_point.activity.name == 'Revisión de Cultivos':
                reference_point.activity.time_required = timedelta(seconds=5)
                reference_point.save()
        
        parcel1 = Parcel.objects.first()

        activity3 = Activity.objects.create(
            name='Control de plagas',
            is_complete=False,
            time_required=timedelta(seconds=6)  
        )
        activity4 = Activity.objects.create(
            name='Análisis de nutrientes',
            is_complete=False,
            time_required=timedelta(seconds=8)  
        )
        reference_point5 = ReferencePoint.objects.create(
            parcel=parcel1,
            location=Point(37.69447, -122.44579),  # Ubicación del punto de referencia
            activity=activity3
        )
        reference_point6 = ReferencePoint.objects.create(
            parcel=parcel1,
            location=Point(37.69437, -122.44565),  # Ubicación del punto de referencia
            activity=activity4
        )

        self.stdout.write(self.style.SUCCESS(f'Actividad creada exitosamente.'))