# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 01:10:36 2017

@author: miannuzzi
"""

import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('ggplot')

weather = pd.read_csv('weather.csv', low_memory=False)
trips = pd.read_csv('trip.csv', low_memory=False)
stations = pd.read_csv('station.csv', low_memory=False)
# weather = weather[weather["zip_code"] == 94107]


def prepro_trips():
    # crea la columna date con tipo datetime y nuevas columnas para analizar despues
    trips["date"] = pd.to_datetime(trips.start_date, format='%m/%d/%Y %H:%M')
    trips["month"] = trips["date"].apply(lambda x: x.month)
    trips["day"] = trips["date"].apply(lambda x: x.day)
    trips["hour"] = trips["date"].apply(lambda x: x.hour)
    trips["year"] = trips["date"].apply(lambda x: x.year)
    trips["DATE"] = pd.to_datetime(trips[['year', 'month', 'day']], yearfirst=True)
    trips["trips"] = trips["day"].apply(lambda x: 1)
    trips["recorrido"] = trips["start_station_name"] + " to " + trips["end_station_name"]


def prepro_trips_agus():
    # crea la columna date con tipo datetime y nuevas columnas para analizar despues
    trips["date"] = pd.to_datetime(trips.start_date, format='%m/%d/%Y %H:%M')
    trips["month"] = trips["date"].apply(lambda x: x.month)
    trips["day"] = trips["date"].apply(lambda x: x.day)
    trips['weekday'] = trips['date'].apply(lambda x: x.weekday())
    trips["hour"] = trips["date"].apply(lambda x: x.hour)
    trips["year"] = trips["date"].apply(lambda x: x.year)
    trips["DATE"] = pd.to_datetime(trips[['year', 'month', 'day']], yearfirst=True)
    trips["trips"] = trips["day"].apply(lambda x: 1)
    trips["recorrido"] = trips["start_station_name"] + " to " + trips["end_station_name"]


def prepro_cities():
#    zip_codes = weather.zip_code.unique()
 #   cities = stations.city.unique()
    dict = {"city":['San Jose', 'Redwood City', 'Mountain View', 'Palo Alto', 'San Francisco'],
            "zip_code":[95113, 94063, 94041, 94301, 94017]}
    return pd.DataFrame(dict)
    
    
def combinar_city_weather(weather, cities):
    return pd.merge(weather, cities,on="zip_code", how="inner") # left_on='zip_code', right_on='zip_code')
    
def combinar_station_weather(weather, stations):
    return pd.merge(weather, stations,on="city", how="inner")
    
def combinar_trips_weather():
    clima = prepro_clima()
    cities = prepro_cities()
    merged_cities = combinar_city_weather(clima, cities)
    merged_stations = combinar_station_weather(merged_cities, stations)
    return pd.merge(merged_stations, trips, left_on='id', right_on='start_station_id')
    

def prepro_clima():
    clima = pd.DataFrame()#columns=['date', 'month', 'day', 'year', 'max_temperature_f'])
    clima["date"] = pd.to_datetime(weather.date, format="%m/%d/%Y")    
#    weather['DATE'] = pd.to_datetime(weather[['year', 'month', 'day']], yearfirst=True)
    
    clima["max_temperature_f"] = weather["max_temperature_f"].apply(lambda x: (x - 32) / 1.8)
    clima["max_visibility_miles"] = weather["max_visibility_miles"]
    clima["max_dew_point_f"] = weather["max_dew_point_f"]
    clima["max_humidity"] = weather["max_humidity"]
    
    clima["precipitation_inches"] = pd.to_numeric(weather["precipitation_inches"], errors="coerce")
    #weather["llueve"] = weather["precipitation_inches"].apply(lambda x: 0 if x == 0.0 else 1)
  #  weather["llueve"] = weather["events"].apply(lambda x: 1 if ("rain" in x) else 0)
   # weather["niebla"] = weather["events"].apply(lambda x: 1 if ("fog" in x) else 0)
   # clima["dias_lluvia"] = weather["precipitation_inches"].apply(lambda x: 1)
    clima["zip_code"] = weather["zip_code"]
    return clima
    
def graficar_evolucion_clima_max_date():
    clima = prepro_clima()
    cities = prepro_cities()
    merged_cities = combinar_city_weather(clima, cities)
    
    max_date = pd.to_datetime(weather.date.max(), format="%m/%d/%Y")
    weather_aux = clima[clima["date"] == max_date]
    merged_cities = combinar_city_weather(weather_aux, cities)
    merged_cities = merged_cities[["max_temperature_f", "max_visibility_miles", "max_dew_point_f", "max_humidity", "precipitation_inches","city"]]
    merged_cities.plot(subplots=True)
    
    #labels = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
    plt.title("Evolucion de variables climáticas según código postal.")
    plt.xlabel("Ciudad")
    
    
    #plt.xticks(index, labels)
    plt.show()
    
    




#graficar_estaciones_entregadoras_y_receptoras()
graficar_evolucion_clima_max_date()


#print(combinar_trip_weather().head(4))


