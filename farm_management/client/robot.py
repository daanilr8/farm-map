import time
import math
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import requests
from queue import Queue
import threading

class Robot:
    def __init__(self, name: str):
        self.name = name
        self.lat = 37.69428 # Latitude HOME
        self.lng = -122.44586 # Longitude HOME
        self.orientation = 30 # Orientation HOME
        self.target_coordinates_queue = Queue() 

    def calculate_bearing(self, target_lat, target_lng):
        # Convertir de grados a radianes
        latA_rad = math.radians(self.lat)
        lngA_rad = math.radians(self.lng)
        latB_rad = math.radians(target_lat)
        lngB_rad = math.radians(target_lng)

        # Diferencia de longitud
        delta_lng = lngB_rad - lngA_rad

        # Fórmula del bearing
        x = math.sin(delta_lng) * math.cos(latB_rad)
        y = math.cos(latA_rad) * math.sin(latB_rad) - math.sin(latA_rad) * math.cos(latB_rad) * math.cos(delta_lng)

        bearing_rad = math.atan2(x, y)

        # Convertir de radianes a grados
        bearing_deg = (math.degrees(bearing_rad) + 360) % 360

        return bearing_deg

    def calculate_route(self, target_lat, target_lng):
        latStep = (target_lat - self.lat) / 10
        lngStep = (target_lng - self.lng) / 10

        for i in range(10):
            self.lat += latStep
            self.lng += lngStep

            if i < 9:
                self.orientation = self.calculate_bearing(target_lat, target_lng)
            # Hacer una pausa de 1 segundo
            self.upload_to_db()
            time.sleep(1)

    def add_target_coordinate_to_queue(self, lat, lng):
        self.target_coordinates_queue.put((lat,lng))

    def upload_to_db(self):
        response_data = {
            'name' : self.name,
            'lat': self.lat,
            'lng' : self.lng,
            'orientation' : self.orientation
        }
        print(response_data)

        # Enviar el punto de la ruta 
        url = 'http://127.0.0.1:8000/post-rover-data/'
        response = requests.post(url, json=response_data)
        # Verificar la respuesta
        if response.status_code == 200:
            print('Solicitud exitosa con lng:', self.lng)
            print('Solicitud exitosa con lat:', self.lat)
            print('Solicitud exitosa con orient:', self.orientation)
        else:
            print('Error en la solicitud:', response.status_code, response.text)
    def start_navigate_robot(self):
        # Iniciar el hilo que está revisando continuamente la cola de coordenadas
        navigation_thread = threading.Thread(target=self._navigate_loop)
        navigation_thread.daemon = True  # Para que se cierre al terminar el programa
        navigation_thread.start()

    def _navigate_loop(self):
        while True:
            if not self.target_coordinates_queue.empty():
                target_lat, target_lng = self.target_coordinates_queue.get()
                print(f"Calculando ruta hacia lat: {target_lat}, lng: {target_lng} desde lat:" + str(self.lat) + " y desde lng: " + str(self.lng))
                self.calculate_route(target_lat, target_lng)
            else:
                time.sleep(0.1)