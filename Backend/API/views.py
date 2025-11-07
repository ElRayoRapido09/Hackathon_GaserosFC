from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests
import time
from django.conf import settings
from django.utils import timezone

from .models import FlightSnapshot, FlightState
from .serializers import FlightSnapshotSerializer, FlightStateSerializer  # Importa los serializers


# Función para obtener token OAuth2
def get_opensky_token():
    url = "https://auth.opensky-network.org/auth/realms/opensky-network/protocol/openid-connect/token"
    data = {
        'grant_type': 'client_credentials',
        'client_id': 'gaserosfc-api-client',
        'client_secret': 'GPsfDsxv8i8MAj9PPN1OEUERM9HhzdCU'
    }
    response = requests.post(url, data=data, timeout=10)
    response.raise_for_status()
    return response.json()['access_token']


@api_view(['GET'])  # Removí @require_GET y @csrf_exempt
def get_active_flights(request):
    """
    Obtiene vuelos activos de OpenSky y opcionalmente los guarda en DB.
    """
    save_to_db = request.GET.get('save_to_db', 'false').lower() == 'true'
    
    try:
        # Llama a OpenSky API
        response = requests.get('https://opensky-network.org/api/states/all', timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if save_to_db:
            # Crea un snapshot
            snapshot = FlightSnapshot.objects.create(
                time=data.get('time', int(time.time())),
                total_states=len(data.get('states', []))
            )
            
            # Guarda cada estado de vuelo
            for state in data.get('states', []):
                FlightState.objects.create(
                    snapshot=snapshot,
                    icao24=state[0],
                    callsign=state[1],
                    origin_country=state[2],
                    time_position=state[3],
                    last_contact=state[4],
                    longitude=state[5],
                    latitude=state[6],
                    baro_altitude=state[7],
                    on_ground=state[8],
                    velocity=state[9],
                    true_track=state[10],
                    vertical_rate=state[11],
                    sensors=state[12],
                    geo_altitude=state[13],
                    squawk=state[14],
                    spi=state[15],
                    position_source=state[16],
                )
        
        # Devuelve los datos actuales
        return Response(data, status=status.HTTP_200_OK)
    except requests.RequestException as e:
        return Response({'error': f'Error al obtener datos de OpenSky: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_and_save_flights(request):
    """
    Alias para get_active_flights (guarda datos por defecto).
    """
    # Redirige a get_active_flights con save_to_db=true
    request.GET = request.GET.copy()
    request.GET['save_to_db'] = 'true'
    return get_active_flights(request)


@api_view(['GET'])
def get_snapshots(request):
    """
    Obtiene snapshots de vuelos guardados en la DB.
    """
    limit = request.GET.get('limit', None)
    try:
        snapshots = FlightSnapshot.objects.all().order_by('-time')
        if limit:
            snapshots = snapshots[:int(limit)]
        
        serializer = FlightSnapshotSerializer(snapshots, many=True)
        return Response({'snapshots': serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)