import pandas as pd
from datetime import datetime
import KN309TarasHrechukh2


def date_converter_and_to_index(dataframe):
    dataframe = dataframe.rename(columns={'day/month': 'Date'})
    dataframe['Date'] = dataframe['Date'] + '.2019'
    dataframe = dataframe.set_index('Date')
    return dataframe


def time_converter(time):
    return datetime.strftime(datetime.strptime(time, "%I:%M %p"), "%H:%M")


def humidity_to_int(percentage):
    return percentage[:-1]


def speed_to_int(speed):
    return speed[:-5]


def pressure_to_float(pressure):
    return pressure.replace(",", ".")


dataframe = pd.read_csv("DATABASE.csv", sep=";")
dataframe = date_converter_and_to_index(dataframe)

for i in range(len(dataframe['Time'])):
    dataframe['Time'][i] = dataframe['Time'][i].replace(dataframe['Time'][i], time_converter(dataframe['Time'][i]))
    dataframe['Humidity'][i] = int(dataframe['Humidity'][i].replace(dataframe['Humidity'][i], humidity_to_int(dataframe['Humidity'][i])))
    dataframe['Wind Speed'][i] = int(dataframe['Wind Speed'][i].replace(dataframe['Wind Speed'][i], speed_to_int(dataframe['Wind Speed'][i])))
    dataframe['Wind Gust'][i] = int(dataframe['Wind Gust'][i].replace(dataframe['Wind Gust'][i], speed_to_int(dataframe['Wind Gust'][i])))
    dataframe['Pressure'][i] = float(dataframe['Pressure'][i].replace(dataframe['Pressure'][i], pressure_to_float(dataframe['Pressure'][i])))

KN309TarasHrechukh2.data_visualizer(dataframe)
