from rest_framework import serializers


class Weather(serializers.Serializer):
    dt = serializers.DateField(required=False)
    city = serializers.CharField()
