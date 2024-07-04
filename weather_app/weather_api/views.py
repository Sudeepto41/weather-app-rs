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
    
    aqi_index_measures = {
        "1": "Good",
        "2": "Fair",
        "3": "Moderate",
        "4": "Poor",
        "5": "Very Poor"
    }

    data = {
        "current_weather": {
            "city": str(city),
            "temperature": weather_resp['current']['temperature_2m'],
            "humidity": weather_resp['current']['relative_humidity_2m'],
            "wind_speed": weather_resp['current']['wind_speed_10m'],
            "precipitation": weather_resp['current']['precipitation'],
            "is_day": "Day" if weather_resp['current']['is_day'] else  "Night"
        },    
        "air_quality": {
            'aqi': air_resp['list'][0]['main']['aqi'],
            'aqi_measure': aqi_index_measures[str(air_resp['list'][0]['main']['aqi'])],
            'co': air_resp['list'][0]['components']['co'],
            'no': air_resp['list'][0]['components']['no'],
            'no2': air_resp['list'][0]['components']['no2'],
            'o3': air_resp['list'][0]['components']['o3'], 
            'so2': air_resp['list'][0]['components']['so2'], 
            'pm2_5': air_resp['list'][0]['components']['pm2_5'], 
            'pm10': air_resp['list'][0]['components']['pm10'], 
            'nh3': air_resp['list'][0]['components']['nh3'],
        },
        "past": [
            {
                'date': weather_resp['daily']['time'][0],
                'temp_max': weather_resp['daily']['temperature_2m_max'][0],
                'temp_min': weather_resp['daily']['temperature_2m_min'][0],
            },
            {
                'date': weather_resp['daily']['time'][1],
                'temp_max': weather_resp['daily']['temperature_2m_max'][1],
                'temp_min': weather_resp['daily']['temperature_2m_min'][1],
            },
            {
                'date': weather_resp['daily']['time'][2],
                'temp_max': weather_resp['daily']['temperature_2m_max'][2],
                'temp_min': weather_resp['daily']['temperature_2m_min'][2],
            },
            
        ],
        "future": [
            {
                'date': weather_resp['daily']['time'][4],
                'temp_max': weather_resp['daily']['temperature_2m_max'][4],
                'temp_min': weather_resp['daily']['temperature_2m_min'][4],
            },
            {
                'date': weather_resp['daily']['time'][5],
                'temp_max': weather_resp['daily']['temperature_2m_max'][5],
                'temp_min': weather_resp['daily']['temperature_2m_min'][5],
            },
            {
                'date': weather_resp['daily']['time'][6],
                'temp_max': weather_resp['daily']['temperature_2m_max'][6],
                'temp_min': weather_resp['daily']['temperature_2m_min'][6],
            },
        ]
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
        "timezone": "auto",
        "past_days": 3,
        "forecast_days": 4,
	    "current": [
            "temperature_2m", 
            "relative_humidity_2m", 
            "is_day", 
            "precipitation", 
            "wind_speed_10m"
        ],
        "daily": [
            "temperature_2m_max", 
            "temperature_2m_min"
        ],
    }
    response = requests.get(weather_base_url, params=params).json()
    print(response)
    return response

def get_air_quality(lat: str, long: str) -> dict:
    air_url = air_base_url.format(lat, long, API_KEY)
    response = requests.get(air_url).json()
    return response