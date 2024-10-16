import time
import math
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import requests
from robot import Robot


robot = Robot(name="Rover 1")
robot.start_navigate_robot()

# TODO: How to start BaseHTTPRequestHanlder with robot name + START ROBOT THREAD calling start_robot
class RobotClient(BaseHTTPRequestHandler):
    def __init__(self, *args, robot_name=None, **kwargs):
        super().__init__(*args, **kwargs)

    def do_POST(self):
        # Obtener la longitud de los datos enviados en el cuerpo de la solicitud
        content_length = int(self.headers['Content-Length'])
        
        # Leer los datos enviados en el cuerpo de la solicitud
        post_data = self.rfile.read(content_length)
        
        # Decodificar los datos
        try:
            data = json.loads(post_data.decode('utf-8'))
            print(f"Datos recibidos: {data}")

            endLat = data.get('endLat')
            endLng = data.get('endLng')
            
            # Responder con un mensaje JSON
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"OK": "Se recibieron los datos correctamente"}
            self.wfile.write(json.dumps(response).encode('utf-8'))

            route = robot.add_target_coordinate_to_queue(float(endLat),float(endLng))
                
        except json.JSONDecodeError:
            # En caso de error al decodificar los datos
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"error": "No se pudieron decodificar los datos JSON"}
            self.wfile.write(json.dumps(response).encode('utf-8'))


    # Función de fábrica para pasar el nombre del robot
def create_robot_client(robot_name):
    def handler(*args, **kwargs):
        RobotClient(*args, robot_name=robot_name, **kwargs)
    return handler

    # Configurar el servidor para escuchar en el puerto 8080
def run(server_class=HTTPServer, port=8080):
    server_address = ('', port)
    # handler = create_robot_client(robot_name)  # Pasar el nombre del robot
    httpd = server_class(server_address, RobotClient)
    print(f'Servidor corriendo en el puerto {port} con el robot ')
    httpd.serve_forever()

if __name__ == '__main__':
    run()