from django.shortcuts import render
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET


@require_GET
@csrf_exempt  # Eliminar en producción; usar manejo adecuado de CSRF
def get_active_flights(request):
    """
    Obtener vuelos activos de la API de OpenSky, con filtros opcionales.
    Endpoint de API: https://opensky-network.org/api/states/all
    Parámetros opcionales: origin_country (ej. ?origin_country=Spain)
    """
    url = "https://opensky-network.org/api/states/all"
    params = {}
    
    # Agregar filtros desde los parámetros de la URL
    origin_country = request.GET.get('origin_country')
    if origin_country:
        params['origin_country'] = origin_country
    
    # Puedes agregar más filtros aquí, como bounding box
    # lamin = request.GET.get('lamin')  # Latitud mínima
    # etc.
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Filtrar adicionalmente en Python si es necesario (por ejemplo, por altitud)
        altitude_min = request.GET.get('altitude_min')
        if altitude_min:
            try:
                alt_min = float(altitude_min)
                filtered_states = [state for state in data.get('states', []) if state[7] and state[7] > alt_min]
                data['states'] = filtered_states
            except ValueError:
                pass  # Ignorar si no es un número válido
        
        return JsonResponse(data)
    except requests.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)