import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt


weather = pd.read_csv('weather.csv', low_memory=False)
trips = pd.read_csv('trip.csv', low_memory=False)

#print(trips["duration"].max())


def prepro():
    del weather["events"]
    del weather["precipitation_inches"]
    del weather["zip_code"]
    del weather["date"]
    weather["max_temperature_f"] = weather["max_temperature_f"].apply(lambda x: (x - 32) / 1.8)
    weather["mean_temperature_f"] = weather["mean_temperature_f"].apply(lambda x: (x - 32) / 1.8)
    weather["min_temperature_f"] = weather["min_temperature_f"].apply(lambda x: (x - 32) / 1.8)
    weather["max_dew_point_f"] = weather["max_dew_point_f"].apply(lambda x: (x - 32) / 1.8)
    weather["mean_dew_point_f"] = weather["mean_dew_point_f"].apply(lambda x: (x - 32) / 1.8)
    weather["mean_dew_point_f"] = weather["mean_dew_point_f"].apply(lambda x: (x - 32) / 1.8)
    weather["min_dew_point_f"] = weather["min_dew_point_f"].apply(lambda x: (x - 32) / 1.8)

    keys = weather.columns.values
    dic_max, dic_min, dic_mean, dic_mad, dic_median = {}, {}, {}, {}, {}
    for key in keys :
        dic_max[key] = weather[key].max()
        dic_min[key] = weather[key].min()
        dic_mean[key] = weather[key].mean()
        dic_mad[key] = weather[key].mad()
        dic_median[key] = weather[key].median()
    return dic_mad, dic_mad, dic_mean, dic_max, dic_median


dic_mad, dic_min, dic_mean, dic_max, dic_median = prepro()
"""
print("max_temp")
print(dic_max)
print("min_temp")
print(dic_min)
print("mad_temp")
print(dic_mad)
print("median temp")
print(dic_median)
print("mean_temp")
print(dic_mean)
"""
def maximas_temps():
    index = [int(dic_max["max_temperature_f"]),int( dic_min["max_temperature_f"]),int( dic_mean["max_temperature_f"]),int( dic_mad["max_temperature_f"]),int( dic_median["max_temperature_f"])]
    labels = ["maxima", "minima", "media", "desviacion media", "mediana"]
    plt.title("maximas temperaturas")
    plt.xlabel("Funciones")
    plt.bar([0,1,2,3,4], index, align="center")
    plt.xticks([0,1,2,3,4], labels)
    plt.show()
maximas_temps()

