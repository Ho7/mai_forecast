import datetime
import requests
import json

from django.conf import settings


class ForecastError(Exception):
    def __init__(self, info, *args, **kwargs):
        self.info = info


class Forecast:
    def __init__(self, city: str, date: datetime.date = None):
        self.city = city
        self.date = date

        if self.date:
            self.date = self.date.isoformat()

    def get_weather(self):
        result = {
            'city': self.city,
            'unit': self.get_temperature_unit(),
            'temperature': '',
        }

        city_coords = self._get_city_coords()

        if self.date:
            date = datetime.datetime.strptime(self.date, '%Y-%m-%d').timestamp().as_integer_ratio()[0]

            response = requests.get(self.get_weather_url() +
                                    f'/{self.get_weather_token()}/{city_coords[0]},{city_coords[1]},{date}', params=self.get_weather_params())
        else:
            response = requests.get(self.get_weather_url() +
                                    f'/{self.get_weather_token()}/{city_coords[0]},{city_coords[1]}', params=self.get_weather_params())

        if response.status_code >= 300:
            raise ForecastError('Ошибка получения прогноза: %s' % response.text)

        response_text_dict = json.loads(response.text)

        result['temperature'] = response_text_dict['currently']['temperature']

        return result

    def _get_city_coords(self):
        response = requests.get(self.get_search_url(), params=self.get_search_params())
        if response.status_code >= 300:
            raise ForecastError('Ошибка поиска города: %s' % response.text)

        response_text_dict = json.loads(response.text)

        lat = response_text_dict['results'][0]['locations'][0]['latLng']['lat']
        lng = response_text_dict['results'][0]['locations'][0]['latLng']['lng']
        return lat, lng

    def get_search_params(self):
        return {'key': self.get_search_token(), 'location': self.city}

    @staticmethod
    def get_weather_url():
        return settings.URL_WEATHER

    @staticmethod
    def get_weather_token():
        return settings.API_TOKEN_WEATHER

    @staticmethod
    def get_search_url():
        return settings.URL_SEARCH_CITY

    @staticmethod
    def get_search_token():
        return settings.API_TOKEN_SEARCH_CITY

    @staticmethod
    def get_weather_params():
        return {'lang': 'ru', 'units': 'si'}

    @staticmethod
    def get_temperature_unit():
        return 'celsius'
