from django.shortcuts import render
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.conf import settings
from django.views.decorators.cache import cache_page
import base64
from .models import FlightSnapshot, FlightState
from django.db import transaction


# Función para obtener token OAuth2
def get_opensky_token():
    url = "https://auth.opensky-network.org/auth/realms/opensky-network/protocol/openid-connect/token"
    data = {
        'grant_type': 'client_credentials',
        'client_id': 'gaserosfc-api-client',  # Asumiendo que es client_id
        'client_secret': 'GPsfDsxv8i8MAj9PPN1OEUERM9HhzdCU'  # Asumiendo que es client_secret
    }
    response = requests.post(url, data=data, timeout=10)
    response.raise_for_status()
    return response.json()['access_token']


@require_GET
@csrf_exempt  # Eliminar en producción; usar manejo adecuado de CSRF
def get_active_flights(request):
    """
    Obtener vuelos activos de la API de OpenSky, con filtros opcionales.
    Automáticamente guarda los datos en la base de datos.
    Endpoint de API: https://opensky-network.org/api/states/all
    Parámetros opcionales: 
        - origin_country (ej. ?origin_country=Spain)
        - save_to_db (ej. ?save_to_db=false para no guardar, por defecto guarda)
    """
    params = {}
    
    # Agregar filtros desde los parámetros de la URL
    origin_country = request.GET.get('origin_country')
    if origin_country:
        params['origin_country'] = origin_country
    
    # Parámetro para decidir si guardar en DB (por defecto True)
    save_to_db = request.GET.get('save_to_db', 'true').lower() != 'false'
    
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
        
        # Guardar automáticamente en la base de datos si no es consulta histórica
        snapshot_info = None
        if save_to_db and not (begin and end):
            try:
                time = data.get('time', 0)
                states = data.get('states', [])
                
                if time and states:
                    snapshot = save_flight_data_to_db(time, states)
                    snapshot_info = {
                        'snapshot_id': snapshot.id,
                        'total_saved': snapshot.total_states,
                        'saved_at': snapshot.created_at.isoformat()
                    }
            except Exception as e:
                print(f"Error guardando en base de datos: {e}")
                # Continuamos devolviendo los datos aunque falle el guardado
        
        # Agregar información del guardado a la respuesta
        if snapshot_info:
            data['db_snapshot'] = snapshot_info
            
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            # Rate limit exceeded, return a message
            return JsonResponse({'error': 'Rate limit exceeded. Please try again later.'}, status=429)
        else:
            raise  # Re-raise other errors
    
    # Para históricos, data es una lista de vuelos; para actuales, es {'time': ..., 'states': [...]}
    return JsonResponse(data)


def save_flight_data_to_db(time, states_list):
    """
    Guarda los datos de vuelos en la base de datos.
    
    Args:
        time: Timestamp Unix del snapshot
        states_list: Lista de estados de vuelos (arrays de 17 elementos)
    
    Returns:
        FlightSnapshot: El snapshot creado con todos sus estados
    """
    with transaction.atomic():
        # Crear el snapshot
        snapshot = FlightSnapshot.objects.create(
            time=time,
            total_states=len(states_list) if states_list else 0
        )
        
        # Crear los estados de vuelos en lote
        flight_states = []
        for state in states_list:
            if state and len(state) >= 17:
                flight_state = FlightState(
                    snapshot=snapshot,
                    icao24=state[0] or '',
                    callsign=state[1].strip() if state[1] else None,
                    origin_country=state[2] or '',
                    time_position=state[3],
                    last_contact=state[4] or 0,
                    longitude=state[5],
                    latitude=state[6],
                    baro_altitude=state[7],
                    on_ground=state[8] or False,
                    velocity=state[9],
                    true_track=state[10],
                    vertical_rate=state[11],
                    sensors=state[12],
                    geo_altitude=state[13],
                    squawk=state[14],
                    spi=state[15] or False,
                    position_source=state[16]
                )
                flight_states.append(flight_state)
        
        # Inserción masiva para mejor rendimiento
        if flight_states:
            FlightState.objects.bulk_create(flight_states, ignore_conflicts=True)
        
        return snapshot


@require_GET
@csrf_exempt
def get_and_save_flights(request):
    """
    Obtener vuelos activos de OpenSky y guardarlos en la base de datos.
    Endpoint: /api/flights/save/
    Parámetros opcionales: origin_country
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
        headers = {}
        print(f"Error obteniendo token: {e}")
    
    try:
        url = "https://opensky-network.org/api/states/all"
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Extraer time y states
        time = data.get('time', 0)
        states = data.get('states', [])
        
        # Guardar en la base de datos
        snapshot = save_flight_data_to_db(time, states)
        
        return JsonResponse({
            'success': True,
            'message': 'Datos guardados exitosamente',
            'snapshot_id': snapshot.id,
            'time': snapshot.time,
            'total_states': snapshot.total_states,
            'created_at': snapshot.created_at.isoformat()
        })
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            return JsonResponse({'error': 'Rate limit exceeded. Please try again later.'}, status=429)
        else:
            return JsonResponse({'error': str(e)}, status=500)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_GET
@csrf_exempt
def get_snapshots(request):
    """
    Obtener lista de snapshots guardados con sus estados.
    Endpoint: /api/snapshots/
    Parámetros opcionales:
        - limit: número de snapshots a retornar (default: 10)
        - snapshot_id: ID específico de un snapshot
    """
    snapshot_id = request.GET.get('snapshot_id')
    limit = int(request.GET.get('limit', 10))
    
    try:
        if snapshot_id:
            # Obtener un snapshot específico con sus estados
            snapshot = FlightSnapshot.objects.prefetch_related('states').get(id=snapshot_id)
            states_data = []
            for state in snapshot.states.all():
                states_data.append({
                    'icao24': state.icao24,
                    'callsign': state.callsign,
                    'origin_country': state.origin_country,
                    'time_position': state.time_position,
                    'last_contact': state.last_contact,
                    'longitude': state.longitude,
                    'latitude': state.latitude,
                    'baro_altitude': state.baro_altitude,
                    'on_ground': state.on_ground,
                    'velocity': state.velocity,
                    'true_track': state.true_track,
                    'vertical_rate': state.vertical_rate,
                    'sensors': state.sensors,
                    'geo_altitude': state.geo_altitude,
                    'squawk': state.squawk,
                    'spi': state.spi,
                    'position_source': state.position_source,
                })
            
            return JsonResponse({
                'snapshot_id': snapshot.id,
                'time': snapshot.time,
                'total_states': snapshot.total_states,
                'created_at': snapshot.created_at.isoformat(),
                'states': states_data
            })
        else:
            # Obtener lista de snapshots (sin estados detallados)
            snapshots = FlightSnapshot.objects.all()[:limit]
            snapshots_data = []
            for snapshot in snapshots:
                snapshots_data.append({
                    'id': snapshot.id,
                    'time': snapshot.time,
                    'total_states': snapshot.total_states,
                    'created_at': snapshot.created_at.isoformat()
                })
            
            return JsonResponse({
                'count': len(snapshots_data),
                'snapshots': snapshots_data
            })
            
    except FlightSnapshot.DoesNotExist:
        return JsonResponse({'error': 'Snapshot no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)