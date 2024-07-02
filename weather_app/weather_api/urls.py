from django.urls import path
from . import views

urlpatterns = [
    path('getweather/', views.index, name='getWeather'),
]