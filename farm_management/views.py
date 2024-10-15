from django.shortcuts import render
from django.core.serializers import serialize
from farm_management.models import Parcel,ReferencePoint,Activity,RoverData
from django.contrib.gis.geos import Point
import json
from django.http import JsonResponse
from django.http import HttpResponse



def get_rover_data(request):

    roverData = RoverData.objects.all()
    roverData_geojson = serialize('geojson', roverData, geometry_field='location')
    return JsonResponse(roverData_geojson,safe=False)

def post_rover_data(request):

    if request.method == 'GET':
        rover_id = request.GET.get('id')  # ID del rover
        rover_name = request.GET.get('name')
        rover_lat = request.GET.get('lat')
        rover_lng = request.GET.get('lng')
        rover_orientation = request.GET.get('orientation')  # Orientación
    
    rover = RoverData.objects.get(name=rover_name)
    new_location = Point(float(rover_lng),float(rover_lat))
    rover.location = new_location
    rover.orientation = rover_orientation
    rover.save()
    return HttpResponse('Nuevo parametro añadido')

def rover_map(request):

    return render (request,'map.html')

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
