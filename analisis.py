import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

plt.style.use('ggplot')

weather = pd.read_csv('weather.csv', low_memory=False)
trips = pd.read_csv('trip.csv', low_memory=False)
stations = pd.read_csv('station.csv', low_memory=False)


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


def prepro_weather():
    weather["date"] = pd.to_datetime(weather.date, format="%m/%d/%Y")
    weather["month"] = weather["date"].apply(lambda x: x.month)
    weather["day"] = weather["date"].apply(lambda x: x.day)
    weather["year"] = weather["date"].apply(lambda x: x.year)
    weather['DATE'] = pd.to_datetime(weather[['year', 'month', 'day']], yearfirst=True)
    weather["max_temperature_f"] = weather["max_temperature_f"].apply(lambda x: (x - 32) / 1.8)
    weather["llueve"] = weather["precipitation_inches"].apply(lambda x: 0 if x == 0.0 else 1)
    weather["dias_lluvia"] = weather["precipitation_inches"].apply(lambda x: 1)

def cant_viajes_por_mes():
    trips = trips["month"].value_counts(sort=False)
    trips.plot(kind="bar")
    plt.show()


def cant_viajes_por_dia_semana():
    week = [0, 0, 0, 0, 0, 0, 0]
    for day in trips["date"]:
        week[day.weekday()] += 1

    index = [0, 1, 2, 3, 4, 5, 6]
    labels = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
    plt.title("Cantidad total de viajes por dia de la semana")
    plt.xlabel("Dias")
    plt.bar(index, week, align="center")
    plt.xticks(index, labels)
    plt.show()


def combinar_trips_weather(weather, trips):
    return pd.merge(weather, trips, on="DATE", how="right")

def trips_por_hora():
    tripsHora = trips.groupby("hour")
    tripsHora.count()["start_date"].plot(kind="bar")
    plt.title("Cantidad total de viajes por hora")
    plt.show()


def graficar_trips_por_tempdia():

    tripsByDay = pd.DataFrame({"trips": trips.groupby(["DATE"])["trips"].sum()}).reset_index()
    weather = weather[weather.zip_code == 94107]
    new = combinar_trips_weather(weather,tripsByDay)
    new.plot.scatter('max_temperature_f','trips',alpha=0.25,figsize=(12,8))
    plt.show()

def graficar_cantidad_dias_lluvia():
    tripsByDay = pd.DataFrame({"trips": trips.groupby(["DATE"])["trips"].sum()}).reset_index()
    weather = weather[weather.zip_code == 94107]
    new = combinar_trips_weather(weather, tripsByDay)
    dias = new.groupby("llueve").aggregate(sum)
    dias.plot(kind = "bar", y=["trips"])
    plt.show()

prepro_trips()
trips_por_hora()
#rodrigay
print(trips["recorrido"])
print(trips.groupby(["recorrido"]))