from django.shortcuts import render
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.conf import settings
from django.views.decorators.cache import cache_page
import base64


# Función para obtener token OAuth2
def get_opensky_token():
    url = "https://auth.opensky-network.org/auth/realms/opensky-network/protocol/openid-connect/token"
    data = {
        'grant_type': 'client_credentials',
        'client_id': settings.OPENSKY_USERNAME,  # Asumiendo que es client_id
        'client_secret': settings.OPENSKY_PASSWORD  # Asumiendo que es client_secret
    }
    response = requests.post(url, data=data, timeout=10)
    response.raise_for_status()
    return response.json()['access_token']


@require_GET
@csrf_exempt  # Eliminar en producción; usar manejo adecuado de CSRF
@cache_page(600)  # Cachear por 10 minutos para reducir requests
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
    
    # Obtener token OAuth2
    try:
        token = get_opensky_token()
        headers = {'Authorization': f'Bearer {token}'}
    except Exception as e:
        # Si falla, usar acceso básico (sin headers)
        headers = {}
        print(f"Error obteniendo token: {e}")
    
    # Verificar consulta histórica (timestamps begin/end)
    begin = request.GET.get('begin')
    end = request.GET.get('end')
    
    try:
        if begin and end:
            url = f"https://opensky-network.org/api/flights/all?begin={begin}&end={end}"
            # La API histórica no usa params adicionales
            response = requests.get(url, headers=headers, timeout=10)
        else:
            url = "https://opensky-network.org/api/states/all"
            response = requests.get(url, params=params, headers=headers, timeout=10)
        
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            # Rate limit exceeded, return a message
            return JsonResponse({'error': 'Rate limit exceeded. Please try again later.'}, status=429)
        else:
            raise  # Re-raise other errors
    
    # Para históricos, data es una lista de vuelos; para actuales, es {'time': ..., 'states': [...]}
    return JsonResponse(data)