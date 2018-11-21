import datetime
import requests
import json

from hashlib import md5
from redis import Redis

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

        cache_weather = self._get_weather_in_cache()
        if cache_weather:
            return json.dumps(cache_weather.decode('utf-8'))

        self._add_result_in_cache()

        return json.dumps(self._get_weather_from_external_api())

    def _get_weather_from_external_api(self):
        result = {
            'city': self.city,
            'unit': self._get_temperature_unit(),
            'temperature': '',
        }

        city_coords = self._get_city_coords()

        if self.date:
            date = datetime.datetime.strptime(self.date, '%Y-%m-%d').timestamp().as_integer_ratio()[0]

            response = requests.get(self._get_weather_url() +
                                    f'/{self._get_weather_token()}/{city_coords[0]},{city_coords[1]},{date}',
                                    params=self._get_weather_params())
        else:
            response = requests.get(self._get_weather_url() +
                                    f'/{self._get_weather_token()}/{city_coords[0]},{city_coords[1]}',
                                    params=self._get_weather_params())

        if response.status_code >= 300:
            raise ForecastError('Ошибка получения прогноза: %s' % response.text)

        response_text_dict = json.loads(response.text)

        result['temperature'] = response_text_dict['currently']['temperature']

        return result

    def _get_city_coords(self):
        response = requests.get(self._get_search_url(), params=self._get_search_params())
        if response.status_code >= 300:
            raise ForecastError('Ошибка поиска города: %s' % response.text)

        response_text_dict = json.loads(response.text)

        lat = response_text_dict['results'][0]['locations'][0]['latLng']['lat']
        lng = response_text_dict['results'][0]['locations'][0]['latLng']['lng']
        return lat, lng

    def _get_weather_in_cache(self):
        cache_db = self._get_database_for_cache()
        return cache_db.get(self.get_hash_http_params())

    def _add_result_in_cache(self):
        cache_db = self._get_database_for_cache()
        return cache_db.set(self.get_hash_http_params(), str(self._get_weather_from_external_api()))

    def get_hash_http_params(self):
        hashmd5 = ''
        if self.date:
            hashmd5 += md5(self.date.encode('ascii')).hexdigest()
        hashmd5 += md5(self.city.encode('ascii')).hexdigest()
        return hashmd5

    def _get_search_params(self):
        return {'key': self._get_search_token(), 'location': self.city}

    @staticmethod
    def _get_weather_url():
        return settings.URL_WEATHER

    @staticmethod
    def _get_weather_token():
        return settings.API_TOKEN_WEATHER

    @staticmethod
    def _get_search_url():
        return settings.URL_SEARCH_CITY

    @staticmethod
    def _get_search_token():
        return settings.API_TOKEN_SEARCH_CITY

    @staticmethod
    def _get_weather_params():
        return {'lang': 'ru', 'units': 'si'}

    @staticmethod
    def _get_temperature_unit():
        return 'celsius'

    @staticmethod
    def _get_database_for_cache():
        return Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
