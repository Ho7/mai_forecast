from django.http import JsonResponse
from rest_framework.views import APIView
from core.weather_client import Forecast, ForecastError

from core import serializers


class Weather(APIView):
    serializer_class = serializers.WeatherSerializer

    def get(self, *args, **kwargs):
        serializer = self.get_serializer()
        serializer.is_valid(raise_exception=True)

        city = serializer.validated_data['city']
        date = serializer.validated_data.get('dt')

        forecast = Forecast(city=city, date=date)
        try:
            weather_info = forecast.get_weather()
        except ForecastError as e:
            weather_info = {
                'error': e.info
            }
        return JsonResponse(weather_info)

    def get_serializer(self):
        serializer = self.serializer_class(data=self.request.GET)
        return serializer


