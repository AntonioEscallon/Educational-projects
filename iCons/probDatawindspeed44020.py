from lib2to3.pgen2.pgen import DFAState
import math
import numpy as np
from windpowerlib import WindTurbine
import pandas as pd
from os.path import join, isfile
from os import listdir

#Original files in historic data was changed and so I had to create this new file to make it work with the 
#Edited data. Chris Brie would be so dissapointed in me and how I manipulated the original data (sad face emoji)

date_column = "DATE"
wspd = "RealWSPD"
wspd2 = "WSPD"
windDirection_column = "RealWDIR"
pwr = "PWR"
new_wspd = 'new_wspd'
path = "/Users/antonioescallon23/Documents/GitHub/Educational-projects/iCons/data/station_historic"

def create_df_list(path, items):

    items = [item for item in items if isfile(join(path, item))]
    return items

def probability_calc():
    for items in df:
        for items in second_df:
            #If all of the options are matched then we will check if at that time is greater than the time we thought or not 
            if df[day] == second_df[day] and df[month] == second_df and df[hour] == second_df[hour] and df[minute] == second_df[minute]:
                if df[new_wspd] > second_df[new_wspd]:
                    count += 1
                #We still need to count all the times this data was recorded 
                count_app +=1
        #Adding the historic prob to a new column. This probably has to be changed 
        df["historic_prob"][i] = count/count_app

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