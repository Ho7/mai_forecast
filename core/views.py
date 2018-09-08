import requests
import json

from django.http import HttpResponse


def get_current_weather(request):
    city = request.GET['city']

    forecast = Forecast(city=city)

    return HttpResponse(forecast.get_weather())


def get_weather_for_date(request):
    city = request.GET['city']
    date = request.GET['dt']

    forecast = Forecast(city=city, date=date)

    return HttpResponse(forecast.get_weather())


class Forecast:
    API_TOKEN = '05b0bda0-4da5-46ed-82e4-95de4ec3caef'
    API_TOKEN_SEARCH_CITY = 'Z2MB4Nnp3gP3AGE7y1zmHmbmPZase1KW'
    URL_PATTERN = 'https://api.weather.yandex.ru/v1/forecast'
    URL_PATTERN_SEARCH_CITY = 'http://open.mapquestapi.com/geocoding/v1/batch'
    PARAM = {
        'lang': 'ru_RU',
        'extra': True,
    }

    def __init__(self, city: str = 'Moscow', date: str = None):
        self.city = city
        self.date = date

    def get_weather(self):
        result = {
            'city': self.city,
            'unit': 'celsius',
            'temperature': '',
        }

        coords = self._get_city_coords()
        self.PARAM.update({
            'lat': coords[0],
            'lon': coords[1],
        })

        response = json.loads(
            requests.get(self.URL_PATTERN, params=self.PARAM, headers={'X-Yandex-API-Key': self.API_TOKEN}).text)

        result['temperature'] = response['fact']['temp']

        if self.date:
            date_list = response['forecasts']

            for item in date_list:
                if item['date'] == self.date:
                    result['temperature'] = item['parts']['day']['temp_avg']

        return json.dumps(result)

    def _get_city_coords(self):
        response = json.loads(requests.get(self.URL_PATTERN_SEARCH_CITY,
                                           params={'key': self.API_TOKEN_SEARCH_CITY,
                                                   'location': self.city
                                                   }).text)

        lat = response['results'][0]['locations'][0]['latLng']['lat']
        lng = response['results'][0]['locations'][0]['latLng']['lng']
        return lat, lng
