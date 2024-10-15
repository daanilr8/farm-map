from django.contrib import admin
from farm_management.models import Activity, ReferencePoint,Parcel,RoverData # Asegúrate de importar tus modelos

admin.site.register(RoverData)
admin.site.register(Parcel)  # Registra el modelo Parcel
admin.site.register(Activity)  # Registra el modelo Activity
admin.site.register(ReferencePoint)  # Registra el modelo ReferencePoint

# Register your models here.
