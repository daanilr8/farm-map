import time
import math
from farm_management.send_rover_data import send_request

def calculate_bearing(latA, lngA, latB, lngB):
    # Convertir de grados a radianes
    latA_rad = math.radians(latA)
    lngA_rad = math.radians(lngA)
    latB_rad = math.radians(latB)
    lngB_rad = math.radians(lngB)

    # Diferencia de longitud
    delta_lng = lngB_rad - lngA_rad

    # Fórmula del bearing
    x = math.sin(delta_lng) * math.cos(latB_rad)
    y = math.cos(latA_rad) * math.sin(latB_rad) - math.sin(latA_rad) * math.cos(latB_rad) * math.cos(delta_lng)

    bearing_rad = math.atan2(x, y)

    # Convertir de radianes a grados
    bearing_deg = (math.degrees(bearing_rad) + 360) % 360

    return bearing_deg

def calculate_route(startLat,startLng,endLat,endLng):
    print('Primera iteración: startLng:' + str(startLng) + 'startLat:' + str(startLat) + ' endLng :' + str(endLng) + ' endLat:' + str(endLat))
    latStep = (endLat - startLat) / 10
    lngStep = (endLng - startLng) / 10

    for i in range(11):
        actual_lat = startLat + (latStep * i)
        actual_lng = startLng + (lngStep * i)
        actual_orient = calculate_bearing(actual_lat,actual_lng,endLat,endLng)
        send_request(actual_lng,actual_lat,actual_orient)
        time.sleep(1)
        

