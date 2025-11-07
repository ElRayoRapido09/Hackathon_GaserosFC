from django.contrib import admin
from .models import FlightSnapshot, FlightState


@admin.register(FlightSnapshot)
class FlightSnapshotAdmin(admin.ModelAdmin):
    list_display = ('id', 'time', 'total_states', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('id',)
    ordering = ('-time',)
    readonly_fields = ('created_at',)
    
    def has_add_permission(self, request):
        # Evitar agregar snapshots manualmente, solo desde la API
        return False


@admin.register(FlightState)
class FlightStateAdmin(admin.ModelAdmin):
    list_display = ('id', 'icao24', 'callsign', 'origin_country', 'snapshot', 
                    'latitude', 'longitude', 'baro_altitude', 'on_ground', 'velocity')
    list_filter = ('on_ground', 'origin_country', 'snapshot__created_at')
    search_fields = ('icao24', 'callsign', 'origin_country')
    ordering = ('-snapshot__time', 'icao24')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Información del Snapshot', {
            'fields': ('snapshot',)
        }),
        ('Identificación', {
            'fields': ('icao24', 'callsign', 'origin_country', 'squawk')
        }),
        ('Posición y Tiempo', {
            'fields': ('latitude', 'longitude', 'baro_altitude', 'geo_altitude',
                      'time_position', 'last_contact')
        }),
        ('Movimiento', {
            'fields': ('on_ground', 'velocity', 'true_track', 'vertical_rate')
        }),
        ('Datos Técnicos', {
            'fields': ('sensors', 'spi', 'position_source')
        }),
        ('Metadatos', {
            'fields': ('created_at',)
        }),
    )
    
    def has_add_permission(self, request):
        # Evitar agregar estados manualmente, solo desde la API
        return False
