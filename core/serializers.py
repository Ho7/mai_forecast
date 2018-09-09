from rest_framework import serializers


class WeatherSerializer(serializers.Serializer):
    dt = serializers.DateField(required=False)
    city = serializers.CharField()
