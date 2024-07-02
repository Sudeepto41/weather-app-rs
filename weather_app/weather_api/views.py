import json
import requests
import datetime
from django.shortcuts import render
from django.http import HttpResponse

API_KEY = "2ead5f24ba31456ad6c6d464cc580c92"
geocode_base_url = 'http://api.openweathermap.org/geo/1.0/direct?q={}&appid={}'
weather_base_url = 'https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={}&lon={}&dt={}&appid={}'
dateTime = datetime.datetime.now()

def index(request):
    city = request.GET.get('city').lower()
    lat, long = getGeoLoc(city, API_KEY)
    weather_url = weather_base_url.format(lat, long, dateTime, API_KEY)
    reponse = requests.get(weather_url).json()
    response_body = {
        'Latitude': lat,
        'Longitude': long
    }
    return HttpResponse(str(response_body))


def getGeoLoc(city: str, api_key: str) -> int:
    geo_url = geocode_base_url.format(city, api_key)
    response = requests.get(geo_url).json()
    return response[0]["lat"], response[0]["lon"]