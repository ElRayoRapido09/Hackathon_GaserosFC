from django.db import models


class FlightSnapshot(models.Model):
    """
    Tabla para almacenar el timestamp de cada consulta a la API de OpenSky.
    Cada snapshot puede tener múltiples estados de vuelos asociados.
    """
    time = models.BigIntegerField(
        help_text="Timestamp Unix del momento de la consulta (epoch time)"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha y hora de creación del registro en la base de datos"
    )
    total_states = models.IntegerField(
        default=0,
        help_text="Número total de estados de vuelos en este snapshot"
    )
    
    class Meta:
        db_table = 'flight_snapshots'
        ordering = ['-time']
        indexes = [
            models.Index(fields=['-time']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"Snapshot {self.id} - Time: {self.time}"


class FlightState(models.Model):
    """
    Tabla para almacenar cada estado de vuelo individual de la API de OpenSky.
    Relacionada con FlightSnapshot mediante llave foránea.
    
    Estructura de datos según OpenSky API:
    https://openskynetwork.github.io/opensky-api/rest.html#response
    """
    
    # Relación con el snapshot
    snapshot = models.ForeignKey(
        FlightSnapshot,
        on_delete=models.CASCADE,
        related_name='states',
        help_text="Snapshot al que pertenece este estado de vuelo"
    )
    
    # Campos del array de OpenSky (índices 0-16)
    icao24 = models.CharField(
        max_length=6,
        db_index=True,
        help_text="Código ICAO24 único del transponder (índice 0)"
    )
    callsign = models.CharField(
        max_length=8,
        null=True,
        blank=True,
        db_index=True,
        help_text="Indicativo de llamada del vuelo (índice 1)"
    )
    origin_country = models.CharField(
        max_length=100,
        db_index=True,
        help_text="País de origen del vuelo (índice 2)"
    )
    time_position = models.BigIntegerField(
        null=True,
        blank=True,
        help_text="Timestamp Unix de la última posición (índice 3)"
    )
    last_contact = models.BigIntegerField(
        help_text="Timestamp Unix del último contacto (índice 4)"
    )
    longitude = models.FloatField(
        null=True,
        blank=True,
        help_text="Longitud en grados decimales (índice 5)"
    )
    latitude = models.FloatField(
        null=True,
        blank=True,
        help_text="Latitud en grados decimales (índice 6)"
    )
    baro_altitude = models.FloatField(
        null=True,
        blank=True,
        help_text="Altitud barométrica en metros (índice 7)"
    )
    on_ground = models.BooleanField(
        default=False,
        help_text="Si está en tierra (índice 8)"
    )
    velocity = models.FloatField(
        null=True,
        blank=True,
        help_text="Velocidad en m/s (índice 9)"
    )
    true_track = models.FloatField(
        null=True,
        blank=True,
        help_text="Rumbo verdadero en grados 0-360° (índice 10)"
    )
    vertical_rate = models.FloatField(
        null=True,
        blank=True,
        help_text="Velocidad vertical en m/s (índice 11)"
    )
    sensors = models.JSONField(
        null=True,
        blank=True,
        help_text="Array de IDs de sensores (índice 12)"
    )
    geo_altitude = models.FloatField(
        null=True,
        blank=True,
        help_text="Altitud geométrica en metros (índice 13)"
    )
    squawk = models.CharField(
        max_length=4,
        null=True,
        blank=True,
        help_text="Código transponder squawk (índice 14)"
    )
    spi = models.BooleanField(
        default=False,
        help_text="Si SPI está activo (índice 15)"
    )
    position_source = models.IntegerField(
        null=True,
        blank=True,
        help_text="Fuente de posición: 0=ADS-B, 1=ASTERIX, 2=MLAT (índice 16)"
    )
    
    # Metadatos adicionales
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha y hora de creación del registro"
    )
    
    class Meta:
        db_table = 'flight_states'
        ordering = ['-last_contact', 'icao24']
        indexes = [
            models.Index(fields=['snapshot', 'icao24']),
            models.Index(fields=['snapshot', '-last_contact']),
            models.Index(fields=['callsign']),
            models.Index(fields=['origin_country']),
            models.Index(fields=['on_ground']),
            models.Index(fields=['-last_contact']),
            models.Index(fields=['icao24']),
        ]
        # Evitar duplicados del mismo vuelo en el mismo snapshot
        unique_together = [['snapshot', 'icao24', 'last_contact']]
    
    def __str__(self):
        return f"{self.callsign or 'N/A'} ({self.icao24}) - {self.origin_country}"
