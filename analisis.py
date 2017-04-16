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
lunes, martes, miercoles, jueves, viernes, sabado, domingo = 0,1,2,3,4,5,6
dias = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
meses = ['Enero', 'Febrero', 'Marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre',
              'noviembre', 'diciembre']

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


def prepro_cities():
    #    zip_codes = weather.zip_code.unique()
    #   cities = stations.city.unique()
    dict = {"city": ['San Jose', 'Redwood City', 'Mountain View', 'Palo Alto', 'San Francisco'],
            "zip_code": [95113, 94063, 94041, 94301, 94017]}
    return pd.DataFrame(dict)


def combinar_city_weather(weather, cities):
    return pd.merge(weather, cities, on="zip_code", how="inner")  # left_on='zip_code', right_on='zip_code')


def combinar_station_weather(weather, stations):
    return pd.merge(weather, stations, on="city", how="inner")


def combinar_trips_weather(lista_atributos_weather, lista_atributos_trips ):
    aux_trips_list = ['start_station_id']
    for element in lista_atributos_trips:
        aux_trips_list.append(element)
    trips_aux = trips[aux_trips_list]
    aux_weather_list = ['zip_code', 'DATE']
    for element in lista_atributos_weather:
        aux_weather_list.append(element)
    weather_aux = weather[aux_weather_list]
    stations_aux = stations[['id','city']]
    cities = prepro_cities()
    merged_cities = combinar_city_weather(weather_aux, cities)
    merged_stations = combinar_station_weather(merged_cities, stations_aux)
    return pd.merge(merged_stations, trips_aux, left_on='id', right_on='start_station_id')


def graficar_barra_cant_viajes_por_mes():
    labels = meses
    index = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    trips_month = trips["month"].value_counts(sort=False)
    barras = trips_month.plot(kind="bar")
    barras.set(title = "Cantidad de viajes por mes", xlabel="Meses", ylabel="cantidad de viajes")
    plt.xticks(index,labels)
    plt.show()

def graficar_barra_cant_viajes_por_dia_semana():
    week = [0, 0, 0, 0, 0, 0, 0]
    for day in trips["date"]:
        week[day.weekday()] += 1
    index = [0, 1, 2, 3, 4, 5, 6]
    labels = dias
    plt.title("Cantidad total de viajes por dia de la semana")
    plt.xlabel("Dias de la semana")
    plt.ylabel('Cantidad de viajes')
    plt.bar(index, week, align="center")
    plt.xticks(index, labels)
    plt.show()


def graficar_barra_promedio_temperaturas_promedio_de_dia_en_cada_mes():
    labels = meses
    index = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    weatherbymonth = weather.groupby('month').mean()['mean_temperature_f']
    weatherbymonth.plot(kind= 'bar')
    plt.xticks(index, labels)
    plt.title(" Temperatura promedio del dia por cada mes")
    plt.xlabel("Meses")
    plt.ylabel(' Temperatura promedio del dia [C] ')
    plt.show()


def graficar_barra_cant_viajes_por_hora():
    tripsHora = trips.groupby("hour")
    tripsHora.count()["start_date"].plot(kind="bar")
    plt.title("Cantidad total de viajes por hora")
    plt.xlabel("Hora del dia")
    plt.ylabel('Cantidad de viajes')
    plt.show()

def graficar_barra_cantidad_de_eventos_meteorologicos():
    events = weather.groupby('events').aggregate(sum)['dias_lluvia']
    events.plot(kind='bar')
    plt.title('Cantidad de eventos meteorologicos')
    plt.xlabel('Eventos')
    plt.ylabel('Cantidad de dias que ocurrio')
    plt.show()

def graficar_scatter_weather_by_weekday(atributo_1, atributo_2, lista_de_dias, titulo):

    trips_weather = combinar_trips_weather([atributo_1],[atributo_2])
    trips_weather_weekdays = trips_weather[trips_weather.weekday.isin(lista_de_dias)]
    trips_weather_weekdays =trips_weather_weekdays.groupby('DATE')
    trips_weather_weekdays.plot.scatter(atributo_1, atributo_2, alpha=0.25, figsize=(12,8))
    plt.title(titulo)
    plt.xlabel(atributo_2)
    plt.ylabel(atributo_1)
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
    ranking = cantidad_de_starts.sort_values(by="trips", ascending=False)
    return ranking

def graficar_barra_ranking_recorridos(cantidad_ranking):
    cantidad_de_recorridos = trips[["recorrido","trips"]]
    cantidad_de_recorridos = cantidad_de_recorridos.groupby("recorrido").count()
    ranking_recorridos = cantidad_de_recorridos.sort_values(by = "trips", ascending=False)[:cantidad_ranking]
    ranking_recorridos.plot(kind="bar")
    plt.title('Recorridos mas frecuentes')
    plt.xlabel('Estaciones')
    plt.ylabel('Cantidad de viajes')
    plt.show()

def graficar_cantidad_de_viajes_por_cada_dia_del_set():
    trips_por_dia = trips.groupby('DATE').aggregate(sum)
    trips_por_dia['trips'].plot()
    plt.title('Cantidad de viajes por dia')
    plt.xlabel('Dias')
    plt.ylabel('Cantidad de viajes')
    plt.show()


def graficar_boxplot_cant_viajes_por_dia_de_la_semana():
    aux = {}
    c = 0
    for dia in dias:
        aux[dia] = trips[trips['weekday'] == c ].groupby('DATE').aggregate(sum).reset_index()['trips'][:104]
        c += 1
    aux = pd.DataFrame.from_dict(aux, orient='columns')
    aux.plot.box()
    plt.title('Cantidad de viajes por dia de la semana')
    plt.xlabel('Dias de la semana')
    plt.ylabel('Cantidad de viajes')
    plt.show()

def graficar_boxplot_cant_viajes_por_hora_del_dia():
    aux = {}
    c = 0
    horas = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '15', '16', '17',
             '18', '19', '20', '21','22','23']
    for hora in horas:
        aux[hora] = trips[trips['hour'] == c].groupby('DATE').aggregate(sum).reset_index()['trips'][:104]
        c += 1
    aux = pd.DataFrame.from_dict(aux, orient='columns')
    aux.plot.box()
    plt.title('Cantidad de viajes por hora del dia')
    plt.xlabel('Dias de la semana')
    plt.ylabel('Cantidad de viajes')
    plt.show()

def graficar_scatter_matter(atributo_1, atributo_2, atributo_3, atributo_4):
    tripsByDay = pd.DataFrame({"trips": trips.groupby(["DATE"])["trips"].sum()}).reset_index()
    trips_weather = combinar_trips_weather(weather, tripsByDay)
    trips_weather = trips_weather [["max_temperature_f","min_temperature_f",'precipitation_inches','mean_temperature_f']]
    scatter_matrix(trips_weather, alpha=0.2, figsize=(6, 6), diagonal='kde')
    plt.show()

def graficar_heatmap_viajes_por_hora_en_cada_dia_semana():
    trips3 = trips [["hour",'weekday','trips']]
    trips2 = trips3.pivot_table(index = 'hour',columns = 'weekday',aggfunc=sum )
    fig, ax = plt.subplots(figsize=(16,5))       # Sample figsize in inches
    sns.heatmap(trips2,cmap='Oranges', xticklabels = dias)
    sns.plt.show()

def calcular_top_estaciones_inicio(cantidad_de_estaciones):
    cantidad_de_starts = trips[["start_station_name", "trips"]]
    cantidad_de_starts = cantidad_de_starts.groupby("start_station_name").count()
    ranking = cantidad_de_starts.sort_values(by="trips", ascending=False)[:cantidad_de_estaciones]
    return ranking

def graficar_estaciones_inicio_mas_frecuentes_por_hora(cantidad_de_estaciones):
    lista_top = []
    top_estaciones = calcular_top_estaciones_inicio(cantidad_de_estaciones).reset_index()['start_station_name']
    lista_top = []
    top_estaciones.apply(lambda x: lista_top.append(x))
    trips3 = trips[["hour", 'start_station_name', 'trips']]
    trips3 = trips3[trips3.start_station_name.isin(lista_top)]
    trips2 = trips3.pivot_table(index='hour', columns='start_station_name', aggfunc=sum)
     # Sample figsize in inches
    sns.heatmap(trips2, cmap='Oranges')
    sns.plt.show()

def graficar_correlacion(lista_atributos):
    tripsByDay = pd.DataFrame({"trips": trips.groupby(["DATE"])["trips"].sum()}).reset_index()
    data_estadisticas = combinar_trips_weather(weather, tripsByDay)
    #data_estadisticas = data_estadisticas[['trips','max_temperature_f','min_temperature_f','mean_temperature_f']]
    fig, ax = plt.subplots(figsize=(15,15));        # Sample figsize in inches
    cor = data_estadisticas.loc[:,lista_atributos]\
        .corr().abs()
    sns.heatmap(cor,cmap='Oranges')
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
"""
tripsaux = trips.groupby(['DATE','recorrido']).aggregate(sum).reset_index()

tripsaux['weekday'] = tripsaux['DATE'].apply(lambda x: x.weekday())
tripsaux.plot.scatter('weekday','recorrido',alpha=0.25,figsize=(12,8),s=tripsaux['trips'])
"""


""" como afecta el clima a los viajes """

#graficar_barra_cantidad_de_eventos_meteorologicos()

#graficar_barra_promedio_temperaturas_promedio_de_dia_en_cada_mes()

#lista_de_dias = [lunes, martes, miercoles, jueves, viernes]
#graficar_scatter_weather_by_weekday('max_temperature_f', 'min_temperature_f', lista_de_dias,'grafico')

#atributo_1, atributo_2, atributo_3, atributo_4 = "max_temperature_f","min_temperature_f",'precipitation_inches','mean_temperature_f'
#graficar_scatter_matter( atributo_1, atributo_2, atributo_3, atributo_4 )


""" como cambian los viajes por dia de la semana y hora del dia"""


#graficar_heatmap_viajes_por_hora_en_cada_dia_semana()

#graficar_boxplot_cant_viajes_por_dia_de_la_semana()

#graficar_boxplot_cant_viajes_por_hora_del_dia()

#graficar_barra_ranking_recorridos(4)


"""otros"""

#graficar_barra_cant_viajes_por_dia_semana()

#graficar_barra_cant_viajes_por_mes()

#graficar_cantidad_de_viajes_por_cada_dia_del_set()

#graficar_barra_ranking_recorridos(4)

#lista_atributos = ['max_temperature_f','max_humidity','max_dew_point_f']
#graficar_correlacion(lista_atributos)

#lista_atributos = ['mean_temperature_f','mean_humidity','mean_dew_point_f']
#graficar_correlacion(lista_atributos)

#lista_atributos = ['min_temperature_f','min_humidity','min_dew_point_f']
#graficar_correlacion(lista_atributos

atributos_trips = ['trips']
atributos_weather = ['max_temperature_f']
trips_weather = combinar_trips_weather(atributos_weather, atributos_trips)
print trips_weather.count()

