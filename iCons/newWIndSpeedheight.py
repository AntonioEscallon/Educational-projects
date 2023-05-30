from lib2to3.pgen2.pgen import DFAState
import math
import numpy as np
from windpowerlib import WindTurbine
import pandas as pd
from os.path import join, isfile
from os import listdir

#Original files in historic data was changed and so I had to create this new file to make it work with the 
#Edited data. Chris Brie would be so dissapointed in my and how I manipulated the original data (sad face emoji)

date_column = "DATE"
wspd = "RealWSPD"
wspd2 = "WSPD"
windDirection_column = "RealWDIR"
pwr = "PWR"
new_wspd = 'new_wspd'
path = "/Users/antonioescallon23/Documents/GitHub/Educational-projects/iCons/data/station_historic"


def logLaw(windSpeedR):
    zr = 3    #Reference Height i.e. buoy height (m)
    z0 = 0.0061    #Surface Roughness Factor (m)
    z=150      #Average offshore turbine hub height (m)
    windSpeed = (math.log(z/z0)/math.log(zr/z0))*float(windSpeedR)
    return windSpeed

def vectorConversion(windSpeed, windDireciton):
    u = windSpeed*math.cos(windDireciton)
    v = windSpeed*math.sin(windDireciton)
    return u, v
power_df= 1

def convertFiles(df, new_wspd):
    wind_list = []
    uvector = []
    vvector = []
    #Next 3 lines of code are necessary for becuase I destoryed my data set and I'm a little baby idiot (I'm fixing it tho)
    df["RealWSPD"] = df["WDIR"]
    df["RealWDIR"] = df["WSPD"]
    #new_df = df[["RealWDIR","RealWSPD","GDR","GST","GTIME", "Date", "u", "v" ,"new_wspd", "PWR"]]
    new_df = df.filter(["RealWDIR","RealWSPD","GDR","GST","GTIME", "Date", "u", "v" ,"new_wspd", "PWR"], axis=1)
    #print(new_df)
    for i in range(len(new_df)):
            wind_list.append(round(logLaw(new_df[wspd][i]), 3))
            u , v = vectorConversion(new_df[wspd][i], new_df[windDirection_column][i])
            uvector.append(u)
            vvector.append(v)
    #print(wind_list)
    new_df["u"] = uvector
    new_df["v"] = vvector
    new_df[new_wspd] = wind_list
    #print(power_df)
    power_list = power_converter(new_df, power_df, pwr, new_wspd)
    #print(len(df))
    #print(len(power_list))
    if(len(new_df) != len(power_list)):
        size_df = len(new_df.index) - len(power_list)
        for i in range(size_df):
            power_list.append(0)
    new_df[pwr] = power_list
    return new_df

#POWER CONVERSION STILL DOSNT WORK
def power_converter(df, power_df, pwr, new_wspd):
    power_list = []
    for i in range(len(df)):
        for b in range(len(power_df)):
            #print(df[new_wspd])
            #print(power_df[wspd2])
            #Try except for the index out of range this works and I am a genius and humble god
            try:
                if(df[new_wspd][i] > power_df[wspd2][b] and df[new_wspd][i] < power_df[wspd2][b + 1]):
                    power_list.append(power_df[pwr][b])
            except:
                power_list.append(0)
                print('aha')
                continue 
    return power_list


def convert_stations(df_list, new_wspd, path, month_column, day_column, year_column, hour_column, minute_column):
    count = 1
    for dataframes in df_list:
        print(count)
        #print(df_list)
        #reads all of the chosen stations in the file of csv
        df = pd.read_csv(path + '/' + dataframes, delim_whitespace=True, skiprows= [1])
        df = df.dropna()
        df = df.reset_index()
        #Will convert month colummn into one 
        #df["Date"] = df[month_column] + '/+' +  df[day_column] + '/' + df[year_column]+'/' + df[hour_column] + ':' + df[minute_column]
        #Renaming the fields for each csv 
        df. rename(columns = {year_column :'year', month_column :'month', day_column: 'day', hour_column: 'hour', minute_column: 'minute'}, inplace = True)
        #df["Date"] = pd.to_datetime(df[['year', 'month', 'day', 'hour', 'minute']])
        #Going through power converter 
        new_df = convertFiles(df, new_wspd)
        #Creating a power curve for each station 
        new_df.to_csv(dataframes[:-4] + "pwr22.csv", sep='\t')
        count+=1

def create_df_list(path, items):

    items = [item for item in items if isfile(join(path, item))]
    return items

items = listdir(path)
df_list = create_df_list(path, items)
df = pd.read_csv("/Users/antonioescallon23/Documents/GitHub/Educational-projects/iCons/data/temp44040.csv", sep='\t')
power_df = pd.read_csv("/Users/antonioescallon23/Documents/GitHub/Educational-projects/iCons/data/power_curve2.csv", sep=',')
power_df = power_df[[wspd2, pwr]]
wdir = windDirection_column
month_column, day_column, year_column, hour_column, minute_column = 'MM', 'DD', '#YY',  "hh", 'mm'
convert_stations(df_list, new_wspd, path, month_column, day_column, year_column, hour_column, minute_column)
df = pd.read_csv('/Users/antonioescallon23/Documents/GitHub/Educational-projects/iCons/data/2951440.csv', sep=',')
df = df.dropna(subset=[wspd])
print(df)
df = df.reset_index()
print(type(df))
print(len(df))
df = df[df[wspd].str.contains("s")==False]
df = df.reset_index()
# df2 = convertFiles(df, new_wspd)
# df2.to_csv('station_2951449pwr.csv', sep='\t')
# new_df = convertFiles(df, new_wspd)

# print(new_df)

# new_df.to_csv('station_44040_pwr.csv', sep='\t')

df = pd.read_csv("/Users/antonioescallon23/Documents/GitHub/Educational-projects/iCons/data/station_2951449pwr.csv", sep='\t')

df2 = pd.read_csv("/Users/antonioescallon23/Documents/GitHub/Educational-projects/iCons/data/chosen_stations/44020PWR2.csv")

print(df)
print(df2)
df['DATE'] =  pd.to_datetime(df['DATE'], format='%Y-%m-%dT%H:%M:%S')
df['DATE'] = df['DATE'].dt.strftime('%m/%d/%y %H:%M')
df['Date'] = df['DATE'].str[:-3]
df2['Date'] = df2['Date'].str[:-3]
print(df)

df3 = df.merge(df2, how='left', on='Date')
df3 = df3[df3['PWR_y'].notna()]
print(df3)

df3 = df3[['Date', 'PWR_x', 'PWR_y']]
df3.to_csv('combinedPWR.csv', sep='\t')