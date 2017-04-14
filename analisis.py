import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pandas.tools.plotting import scatter_matrix

plt.style.use('ggplot')

weather = pd.read_csv('weather.csv', low_memory=False)
trips = pd.read_csv('trip.csv', low_memory=False)
stations = pd.read_csv('station.csv', low_memory=False)
weather = weather[weather["zip_code"] == 94107]

def prepro_trips():
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


def prepro_weather():
    weather["date"] = pd.to_datetime(weather.date, format="%m/%d/%Y")
    weather["month"] = weather["date"].apply(lambda x: x.month)
    weather["day"] = weather["date"].apply(lambda x: x.day)
    weather["year"] = weather["date"].apply(lambda x: x.year)
    weather['weekday'] = weather['date'].apply(lambda x: x.weekday())
    weather['DATE'] = pd.to_datetime(weather[['year', 'month', 'day']], yearfirst=True)
    weather["max_temperature_f"] = weather["max_temperature_f"].apply(lambda x: (x - 32) / 1.8)
    weather["min_temperature_f"] = weather["min_temperature_f"].apply(lambda x: (x - 32) / 1.8)
    weather["mean_temperature_f"] = weather["mean_temperature_f"].apply(lambda x: (x - 32) / 1.8)
    weather["precipitation_inches"] = pd.to_numeric(weather["precipitation_inches"], errors="coerce")
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

def graficar_trips_por_hora():
    tripsHora = trips.groupby("hour")
    tripsHora.count()["start_date"].plot(kind="bar")
    plt.title("Cantidad total de viajes por hora")
    plt.show()


def graficar_trips_por_temperatura_dia():
    tripsByDay = pd.DataFrame({"trips": trips.groupby(["DATE"])["trips"].sum()}).reset_index()
    new = combinar_trips_weather(weather,tripsByDay)
    new = new[new['weekday'] ==  0 ]
    new.plot.scatter('max_temperature_f','precipitation_inches',alpha=0.25,figsize=(12,8),s=new['trips'])
    plt.show()


def graficar_cantidad_dias_lluvia():
    tripsByDay = pd.DataFrame({"trips": trips.groupby(["DATE"])["trips"].sum()}).reset_index()
    new = combinar_trips_weather(weather, tripsByDay)
    dias = new.groupby("llueve").aggregate(sum)
    dias.plot(kind = "bar", y=["dias_lluvia"])
    plt.show()


def graficar_viajes_segun_lluvias():
    # df3 = pd.DataFrame(np.random.rand(500, 2), columns=['B', 'C']).cumsum()
    # print df3
    # df3['A'] = pd.Series(list(range(len(df3))))
    # df3.plot(x='A', y='C')
    # plt.show()
    # df = pd.DataFrame({"trips": trips.groupby(["DATE"])["trips"].sum()}).reset_index()
    # print df
    dfw = pd.DataFrame({"weather": weather})
    print dfw

def calcular_top_estaciones_inicio():
    cantidad_de_starts = trips[["start_station_name", "trips"]]
    cantidad_de_starts = cantidad_de_starts.groupby("start_station_name").count()
    ranking = cantidad_de_starts.sort_values(by="trips", ascending=False)[:4]
    return ranking

def graficar_top_recorridos():
    cantidad_de_recorridos = trips[["recorrido","trips"]]
    cantidad_de_recorridos = cantidad_de_recorridos.groupby("recorrido").count()
    ranking_recorridos = cantidad_de_recorridos.sort_values(by = "trips", ascending=False)[:5]
    print(ranking_recorridos)
    ranking_recorridos.plot(kind="bar")
    plt.show()

def graficar_cantidad_de_viajes_por_cada_dia():
    trips_por_dia = trips.groupby('DATE').aggregate(sum)
    trips_por_dia['trips'].plot()
    plt.show()

def graficar_boxplot_dias_totales():
    aux = {}
    dias = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']
    a = 0
    for dia in dias:
        aux[dia] = trips[trips['weekday'] == a].groupby('DATE').aggregate(sum).reset_index()['trips'][:104]
        a += 1

    aux = pd.DataFrame.from_dict(aux,orient='columns')
    aux.plot.box()
    plt.show()
def graficar_scatter_matter():
    tripsByDay = pd.DataFrame({"trips": trips.groupby(["DATE"])["trips"].sum()}).reset_index()
    new = combinar_trips_weather(weather, tripsByDay)
    new2 = new [["max_temperature_f","min_temperature_f",'precipitation_inches','mean_temperature_f']]
    scatter_matrix(new2, alpha=0.2, figsize=(6, 6), diagonal='kde')
    plt.show()

def graficar_heatmap_viajes_por_hora_en_cada_dia_semana():
    trips3 = trips [["hour",'weekday','trips']]
    trips2 = trips3.pivot_table(index = 'hour',columns = 'weekday',aggfunc=sum )
    fig, ax = plt.subplots(figsize=(16,5))       # Sample figsize in inches
    sns.heatmap(trips2,cmap='Oranges', xticklabels = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo'])
    sns.plt.show()

def graficar_estaciones_inicio_por_hora():
    lista_top = []
    top_estaciones = calcular_top_estaciones_inicio().reset_index()['start_station_name']
    lista_top = []
    top_estaciones.apply(lambda x: lista_top.append(x))
    trips3 = trips[["hour", 'start_station_name', 'trips']]
    trips3 = trips3[trips3.start_station_name.isin(lista_top)]
    trips2 = trips3.pivot_table(index='hour', columns='start_station_name', aggfunc=sum)
     # Sample figsize in inches
    sns.heatmap(trips2, cmap='Oranges')
    sns.plt.show()


prepro_trips()
prepro_weather()
"""
def graficar_ranking_de_recorridos_segun_clima():
    tripsByDay = pd.DataFrame({'cantidad_recorridos': trips.groupby(['DATE'])['trips'].sum()}).reset_index()
    trips_recorrido = combinar_trips_weather(trips, tripsByDay)
    trips_weather = combinar_trips_weather(weather, trips_recorrido)
    trips_weather = trips_weather[['recorrido','cantidad_recorridos','max_temperature_f' ]]
    print trips_weather[:10]
    
    ranking_recorridos = cantidad_de_recorridos.sort_values(by="trips", ascending=False)[:5]
    print(ranking_recorridos)
    ranking_recorridos.plot(kind="bar")
    plt.show()

graficar_ranking_de_recorridos_segun_clima()
"""

tripsaux = trips.groupby(['DATE','recorrido']).aggregate(sum).reset_index()

tripsaux['weekday'] = tripsaux['DATE'].apply(lambda x: x.weekday())
tripsaux.plot.scatter('weekday','recorrido',alpha=0.25,figsize=(12,8),s=tripsaux['trips'])



