from django.shortcuts import render
from django.core.serializers import serialize
from farm_management.models import RoverData,Parcel,ReferencePoint,Activity
import json

def map_view(request):
     # Obtener todos los registros de RoverData
    rover_data = RoverData.objects.all()
     # Serializar los datos en formato GeoJSON
    rover_data_geojson = serialize('geojson', rover_data, geometry_field='location')

    hola = "Hola"
    
    return render(request, 'map.html', {'rover_data': rover_data_geojson,'hola':hola})

def farm_map(request):
    # Obtener los puntos de referencia con las actividades relacionadas
    reference_points = ReferencePoint.objects.select_related('activity').all()
    # Crear una lista para serializar manualmente los datos
    reference_points_data = []

    for point in reference_points:
        reference_points_data.append({
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': list(point.location.coords),
            },
            'properties': {
                'id': point.id,
                'parcel': point.parcel.id if point.parcel else None,
                'activity': {
                    'id': point.activity.id if point.activity else None,
                    'name': point.activity.name if point.activity else None,
                    'is_complete': point.activity.is_complete if point.activity else None,
                    'time_required': str(point.activity.time_required) if point.activity else None
                }
            }
        })

    reference_points_data = {
        'type': 'FeatureCollection',
        'features': reference_points_data
    }
    reference_points_geojson = json.dumps(reference_points_data)
    # Obtener todos los registros
    parcels = Parcel.objects.all()
    reference_points_normal = ReferencePoint.objects.all()
     # Serializar los registros en formato geoJSON
    parcels_geojson = serialize('geojson', parcels, geometry_field='boundary')
    reference_p_geojson = serialize('geojson', reference_points_normal, geometry_field='location')

    return render(request,'farm_map.html', {'parcels': parcels_geojson, 'reference_points':reference_points_geojson })
