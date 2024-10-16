from django.contrib.gis.db import models

class Parcel(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Nombre único para la parcela
    boundary = models.PolygonField()  # Campo para definir la geometría de la parcela

    def __str__(self):
        return self.name

class Activity(models.Model):
    name = models.CharField(max_length=100)  # Nombre de la actividad
    is_complete = models.BooleanField(default=False)  # Estado de la actividad (completa o no)
    time_required = models.DurationField()  # Tiempo requerido para la actividad

    def __str__(self):
        return self.name

class ReferencePoint(models.Model):
    parcel = models.ForeignKey(Parcel, on_delete=models.CASCADE, related_name='reference_points')  # Relación con la parcela
    location = models.PointField()  # Campo para la ubicación del punto de referencia
    activity = models.ForeignKey(Activity, on_delete=models.SET_NULL, null=True, blank=True, related_name='reference_points')  # Relación con la actividad


class RoverData(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    location = models.PointField()  # Ubicación del rover
    orientation = models.FloatField()
    status = models.CharField(max_length=20, choices=[
        ('active', 'Activo'),
        ('inactive', 'Inactivo'),
        ('in_mission', 'En Misión'),
    ])
    speed = models.FloatField()  # Velocidad del rover
    timestamp = models.DateTimeField(auto_now=True)