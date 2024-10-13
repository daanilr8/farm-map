from django.contrib.gis.db import models

class RoverData(models.Model):
    name = models.CharField(max_length=100)
    location = models.PointField()  # Ubicación del rover usando datos geoespaciales (lat/lon)
    timestamp = models.DateTimeField(auto_now_add=True)
    
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
