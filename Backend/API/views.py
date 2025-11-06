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
    params = {}
    
    # Agregar filtros desde los parámetros de la URL
    origin_country = request.GET.get('origin_country')
    if origin_country:
        params['origin_country'] = origin_country
    
    # Verificar consulta histórica (timestamps begin/end)
    begin = request.GET.get('begin')
    end = request.GET.get('end')
    if begin and end:
        url = f"https://opensky-network.org/api/flights/all?begin={begin}&end={end}"
        # La API histórica no usa params adicionales
        response = requests.get(url, timeout=10)
    else:
        url = "https://opensky-network.org/api/states/all"
        response = requests.get(url, params=params, timeout=10)
    
    response.raise_for_status()
    data = response.json()
    
    # Para históricos, data es una lista de vuelos; para actuales, es {'time': ..., 'states': [...]}
    return JsonResponse(data)