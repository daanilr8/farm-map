import time
import math
from send_rover_data import send_request
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import requests

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
    route = []
    latStep = (endLat - startLat) / 10
    lngStep = (endLng - startLng) / 10

    for i in range(11):
        actual_lat = startLat + (latStep * i)
        actual_lng = startLng + (lngStep * i)
        actual_orient = calculate_bearing(actual_lat,actual_lng,endLat,endLng)
        route.append([actual_lng,actual_lat,actual_orient])
    
    return route


class MyRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Obtener la longitud de los datos enviados en el cuerpo de la solicitud
        content_length = int(self.headers['Content-Length'])
        
        # Leer los datos enviados en el cuerpo de la solicitud
        post_data = self.rfile.read(content_length)
        
        # Decodificar los datos
        try:
            data = json.loads(post_data.decode('utf-8'))
            print(f"Datos recibidos: {data}")

            startLat = data.get('startLat')
            endLat = data.get('endLat')
            startLng = data.get('startLng')
            endLng = data.get('endLng')
            
            # Responder con un mensaje JSON
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"OK": "Se recibieron los datos correctamente"}
            self.wfile.write(json.dumps(response).encode('utf-8'))

            route = calculate_route(startLat,startLng,endLat,endLng)

            for point in route:

                response_data = {
                    'name' : 'Rover 1',
                    'lat': point[0],
                    'lng' : point[1],
                    'orientation' : point[2]
                }
                print(response_data)

                # Enviar el punto de la ruta 
                url = 'http://127.0.0.1:8000/post-rover-data/'
                response = requests.post(url, json=response_data)
                 # Verificar la respuesta
                if response.status_code == 200:
                    print('Solicitud exitosa con lng:', point[1])
                    print('Solicitud exitosa con lat:', point[0])
                    print('Solicitud exitosa con orient:', point[2])
                else:
                    print('Error en la solicitud:', response.status_code, response.text)
                # Hacer una pausa de 1 segundo
                time.sleep(1)
                
        except json.JSONDecodeError:
            # En caso de error al decodificar los datos
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"error": "No se pudieron decodificar los datos JSON"}
            self.wfile.write(json.dumps(response).encode('utf-8'))

# Configurar el servidor para escuchar en el puerto 8080
def run(server_class=HTTPServer, handler_class=MyRequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Servidor corriendo en el puerto {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
