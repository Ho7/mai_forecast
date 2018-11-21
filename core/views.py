from django.http import HttpResponse
from rest_framework.views import APIView

from mai_forecast import settings
from core.weather_client import Forecast, ForecastError
from core import serializers


class Weather(APIView):
    serializer_class = serializers.WeatherSerializer

    def put(self, *args, **kwargs):
        pass

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
        return HttpResponse(weather_info)

    def get_serializer(self):
        serializer = self.serializer_class(data=self.request.GET)
        return serializer

    @staticmethod
    def redis():
        pass

