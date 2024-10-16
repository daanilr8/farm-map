import requests
import time
import argparse

# Función para enviar la solicitud con parámetros dinámicos
def send_request(lng_value,lat_value,orient_value):
    url = 'http://127.0.0.1:8000/post-rover-data/'

    # Datos a enviar en la solicitud GET, con lng dinámico
    params = {
        'name': 'Rover 1',  # Nombre del rover
        'lat' : lat_value, # Valor dinámico de la latitud
        'lng' : lng_value,  # Valor dinámico de longitud
        'orientation': orient_value  # Orientación del rover
    }

    # Realizar la solicitud GET
    response = requests.post(url, json=params)

    # Verificar la respuesta
    if response.status_code == 200:
        print('Solicitud exitosa con lng:', lng_value)
        print('Solicitud exitosa con lat:', lat_value)
        print('Solicitud exitosa con orient:', orient_value)
    else:
        print('Error en la solicitud:', response.status_code, response.text)

# Función principal que ejecuta la solicitud cada 3 segundos con diferentes valores de lng
def main():
    parser = argparse.ArgumentParser(description='Actualizar los datos del rover.')
    # Hacer que --initial_lng sea opcional, con un valor por defecto
    parser.add_argument('--lng', type=float, default=37.69428, help='Valor inicial de la longitud.')
    parser.add_argument('--lat', type=float, default=-122.44500, help='Valor inicial de la latitud.')
    parser.add_argument('--orient', type=float, default=270.0, help='Valor inicial de la orientación.')
    args = parser.parse_args()

    lng = args.lng
    lat = args.lat
    orient = args.orient
    send_request(lng,lat,orient)
    37.69443
    -122.44570
if __name__ == '__main__':
    main()
