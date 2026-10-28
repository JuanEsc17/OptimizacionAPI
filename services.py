import requests

OSRM_SERVER = "http://router.project-osrm.org"

class OSRMError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

def optimizar_ruta(coordenadas: list[dict]) -> list[dict]:
    """
    Envía las coordenadas al servicio 'trip' de OSRM y devuelve las
    coordenadas de entrada reordenadas según la ruta óptima.
    """
    # Formatear coordenadas a 'lon,lat;lon,lat...' según exige OSRM
    coords_str = ";".join([f"{c['lon']},{c['lat']}" for c in coordenadas])
    url = f"{OSRM_SERVER}/trip/v1/car/{coords_str}"
    params = {
        "source": "first",
        "destination": "last",
        "geometries": "geojson",
        "overview": "full",
        "steps": "false"
    }

    try:
        response = requests.get(url, params=params)
        response_json = response.json()
    except requests.exceptions.RequestException as e:
        raise OSRMError(f"Error de conexión con el servidor de mapas: {str(e)}", status_code=500)

    if response.status_code != 200 or response_json.get("code") != "Ok":
        codigo = response_json.get("code", "Desconocido")
        raise OSRMError(f"Error de OSRM: {codigo}", status_code=400)

    # Ordenar según waypoint_index devuelto por OSRM
    coordenadas_ordenadas = [
        coord for coord, wp in sorted(
            zip(coordenadas, response_json["waypoints"]),
            key=lambda pair: pair[1]["waypoint_index"]
        )
    ]
    return coordenadas_ordenadas
