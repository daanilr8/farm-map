import requests
import time
import argparse

# Función para enviar la solicitud con parámetros dinámicos
def send_request(lng_value,lat_value,orient_value):
    url = 'http://127.0.0.1:8000/post-rover-data/'

    # Datos a enviar en la solicitud GET, con lng dinámico
    params = {
        'id': 1,  # ID del rover
        'name': 'Rover 1',  # Nombre del rover
        'lat' : lat_value,
        'lng' : lng_value,  # Valor dinámico de longitud
        'orientation': orient_value  # Orientación del rover
    }

    # Realizar la solicitud GET
    response = requests.get(url, params=params)

    # Verificar la respuesta
    if response.status_code == 200:
        print('Solicitud exitosa con lng:', lng_value)
    else:
        print('Error en la solicitud:', response.status_code, response.text)

# Función principal que ejecuta la solicitud cada 3 segundos con diferentes valores de lng
def main():
    parser = argparse.ArgumentParser(description='Actualizar los datos del rover.')
    # Hacer que --initial_lng sea opcional, con un valor por defecto
    parser.add_argument('--initial_lng', type=float, default=37.69428, help='Valor inicial de la longitud.')
    parser.add_argument('--initial_lat', type=float, default=-122.44500, help='Valor inicial de la longitud.')
    parser.add_argument('--initial_orient', type=float, default=270.0, help='Valor inicial de la longitud.')
    args = parser.parse_args()

    lng = args.initial_lng
    lat = args.initial_lat
    orient = args.initial_orient

    # Bucle para ejecutar cada 3 segundos
    for _ in range(10):  # Por ejemplo, ejecuta 10 veces
        send_request(lng,lat,orient)
        lng += 0.001  # Cambia el valor de lng en cada iteración
        time.sleep(3)  # Espera 3 segundos antes de la próxima solicitud

if __name__ == '__main__':
    main()
