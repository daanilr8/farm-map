from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.core.serializers import serialize
from farm_management.models import Parcel,ReferencePoint,Activity,RoverData
from django.contrib.gis.geos import Point
import json
from django.http import JsonResponse
from django.http import HttpResponse
import requests


def get_rover_data(request):

    roverData = RoverData.objects.all()
    roverData_geojson = serialize('geojson', roverData, geometry_field='location')
    return JsonResponse(roverData_geojson,safe=False)

@csrf_exempt
def post_rover_data(request):
    
    if request.method == 'POST':
         # Leer el cuerpo de la solicitud como JSON
        data = json.loads(request.body)

        # Extraer los datos del JSON
        rover_name = data.get('name')
        rover_lat = data.get('lat')
        rover_lng = data.get('lng')
        rover_orientation = data.get('orientation')
    
    if rover_name is None or rover_lat is None or rover_lng is None or rover_orientation is None:
        return JsonResponse({'error': 'Faltan parametros'}, status=400)
    
    try:
        rover_string_name = str(rover_name)
        rover = RoverData.objects.get(name=rover_name)
        rover_float_lng = float(rover_lng)
        rover_float_lat = float(rover_lat)
        rover_float_orientation = float(rover_orientation)
        new_location = Point(rover_float_lat,rover_float_lng)
        rover.location = new_location
        rover.orientation = rover_float_orientation
        rover.save()
    except ValueError:
        return JsonResponse({'error': 'Los tipos introducidos son incorrectos.'}, status=400)

    return HttpResponse('Nuevo parametro añadido')

def simulate_rover_movement(request):

    if request.method == 'GET':
        endLat = request.GET.get('endLat')
        endLng = request.GET.get('endLng')

    try:
        endLat = float(endLat)
        endLng = float(endLng)
    except ValueError:
        return JsonResponse({'error': 'Los tipos no son correctos'},status=400)
    
    params = {
        'endLat' : endLat,
        'endLng': endLng
    }
    postUrl = 'http://localhost:8080'
    response = requests.post(postUrl, json=params)

    # Verificar la respuesta
    if response.status_code == 200:
        print('Solicitud exitosa con endLat:', endLat)
        print('Solicitud exitosa con endLng:', endLng)
    else:
        print('Error en la solicitud:', response.status_code, response.text)
    
    return HttpResponse('Simulaton completed')

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
