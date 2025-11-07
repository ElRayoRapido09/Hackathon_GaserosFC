from rest_framework import serializers
from .models import FlightSnapshot, FlightState

class FlightStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightState
        fields = '__all__'

class FlightSnapshotSerializer(serializers.ModelSerializer):
    states = FlightStateSerializer(many=True, read_only=True)

    class Meta:
        model = FlightSnapshot
        fields = '__all__'