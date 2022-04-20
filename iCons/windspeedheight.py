from lib2to3.pgen2.pgen import DFAState
import math
import numpy as np
from windpowerlib import WindTurbine
import pandas as pd
from os.path import join, isfile
from os import listdir

date_column = "Date"
wspd = "WSPD"
wspd2 = "WSPD"
windDirection_column = "WDIR"
pwr = "PWR"
new_wspd = 'new_wspd'
path = "/Users/antonioescallon23/Documents/GitHub/Educational-projects/iCons/data/station_historic"


def logLaw(windSpeedR):
    zr = 9    #Reference Height i.e. buoy height (m)
    z0 = 0.0061    #Surface Roughness Factor (m)
    z=128       #Average offshore turbine hub height (m)
    windSpeed = (np.log(z/z0)/np.log(zr/z0))*windSpeedR
    return windSpeed

def vectorConversion(windSpeed, windDireciton):
    u = windSpeed*math.cos(windDireciton)
    v = windSpeed*math.sin(windDireciton)
    return u, v

def convertFiles(df, new_wspd):
    wind_list = []
    uvector = []
    vvector = []
    for i in range(len(df)):
            wind_list.append(round(logLaw(df[wspd][i]), 0))
            u , v = vectorConversion(df[wspd][i], df[windDirection_column][i])
            uvector.append(u)
            vvector.append(v)
    df['u'] = uvector
    df['v'] = vvector
    df[new_wspd] = wind_list
    power_list = power_converter(df, power_df, pwr, new_wspd, wspd)
    print(len(df))
    print(len(power_list))
    if(len(df) != len(power_list)):
        size_df = len(df.index) - len(power_list)
        for i in range(size_df):
            power_list.append(0)
    df[pwr] = power_list

    return df

def power_converter(df, power_df, pwr, new_wspd, wspd):
    power_list = []
    for i in range(len(df)):
        for b in range(len(power_df)):
            if(df[new_wspd][i] == power_df[wspd][b]):
                power_list.append(power_df[pwr][b])

    return power_list


def convert_stations(df_list, new_wspd, path, month_column, day_column, year_column, hour_column, minute_column):
    count = 1
    for dataframes in df_list:
        print(count)
        df = pd.read_csv(path + '/' + dataframes, delim_whitespace=True, skiprows= [1])
        df = df.dropna()
        df = df.reset_index()
        #df["Date"] = df[month_column] + '/+' +  df[day_column] + '/' + df[year_column]+'/' + df[hour_column] + ':' + df[minute_column]
        df. rename(columns = {year_column :'year', month_column :'month', day_column: 'day', hour_column: 'hour', minute_column: 'minute'}, inplace = True)
        df["Date"] = pd.to_datetime(df[['year', 'month', 'day', 'hour', 'minute']])
        new_df = convertFiles(df, new_wspd)
        new_df.to_csv(dataframes[:-4] + "pwr.csv", sep='\t')
        count+=1

def create_df_list(path, items):

    items = [item for item in items if isfile(join(path, item))]
    return items

items = listdir(path)
df_list = create_df_list(path, items)
# df = pd.read_csv("/Users/antonioescallon23/Documents/GitHub/Educational-projects/iCons/temp44040.csv", sep='\t')
power_df = pd.read_csv("/Users/antonioescallon23/Documents/GitHub/Educational-projects/iCons/data/power_curve2.csv", sep=',')
power_df = power_df[[wspd2, pwr]]
wdir = windDirection_column
month_column, day_column, year_column, hour_column, minute_column = 'MM', 'DD', '#YY',  "hh", 'mm'
convert_stations(df_list, new_wspd, path, month_column, day_column, year_column, hour_column, minute_column)

# new_df = convertFiles(df, new_wspd)

# print(new_df)

# new_df.to_csv('station_44040_pwr.csv', sep='\t')
