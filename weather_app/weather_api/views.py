import json
import requests
import datetime
from django.shortcuts import render
from django.http import HttpResponse
API_KEY = "2ead5f24ba31456ad6c6d464cc580c92"
geocode_base_url = 'http://api.openweathermap.org/geo/1.0/direct?q={}&appid={}'
weather_base_url = "https://api.open-meteo.com/v1/forecast"
air_base_url = 'http://api.openweathermap.org/data/2.5/air_pollution?lat={}&lon={}&appid={}'
dateTime = datetime.datetime.now()

#TODO:
#implement polutant status high low adrak lasun

def index(request):
    city = request.GET.get('city')
    lat, long = getGeoLoc(city, API_KEY)
    weather_resp = get_weather(lat, long)
    air_resp = get_air_quality(lat, long)
    
    print(weather_resp)
    print(air_resp)
    
    data = {
        "current_weather": {
            "city": str(city),
            "temperature": weather_resp['current']['temperature_2m'],
            "humidity": weather_resp['current']['relative_humidity_2m'],
            "wind_speed": weather_resp['current']['wind_speed_10m'],
            "precipitation": weather_resp['current']['precipitation'],
            "is_day": weather_resp['current']['is_day']
        },    
        "air_quality": {
            'aqi': air_resp['list'][0]['main']['aqi'],
            'co': air_resp['list'][0]['components']['co'],
            'no': air_resp['list'][0]['components']['no'],
            'no2': air_resp['list'][0]['components']['no2'],
            'o3': air_resp['list'][0]['components']['o3'], 
            'so2': air_resp['list'][0]['components']['so2'], 
            'pm2_5': air_resp['list'][0]['components']['pm2_5'], 
            'pm10': air_resp['list'][0]['components']['pm10'], 
            'nh3': air_resp['list'][0]['components']['nh3'],
        }
    }

    return HttpResponse(json.dumps( data ))

def getGeoLoc(city: str, api_key: str) -> int:
    geo_url = geocode_base_url.format(city, api_key)
    response = requests.get(geo_url).json()
    return response[0]["lat"], response[0]["lon"]

def get_weather(lat:str, long: str) -> dict:
    params = {
	    "latitude": lat,
	    "longitude": long,
	    "current": [
            "temperature_2m", 
            "relative_humidity_2m", 
            "is_day", 
            "precipitation", 
            "wind_speed_10m"
        ]
    }
    response = requests.get(weather_base_url, params=params).json()
    return response

def get_air_quality(lat: str, long: str) -> dict:
    air_url = air_base_url.format(lat, long, API_KEY)
    response = requests.get(air_url).json()
    return response

def get_status(measure_name:str, measure: int) -> str:
    permissable_limit = {
        'aqi': 0,
        'co': 0,
        'no': 0,
        'no2': 0,
        'o3': 0, 
        'so2': 0, 
        'pm2_5': 0, 
        'pm10': 0, 
        'nh3': 0,
    }