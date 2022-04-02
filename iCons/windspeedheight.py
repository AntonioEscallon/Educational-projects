import math
import numpy as np
from windpowerlib import WindTurbine
import pandas as pd


date_column = "Date"
windSpeed_column = "WSPD"
windDirection_column = "WDIR"
df = pd.read_csv("/Users/antonioescallon23/Documents/GitHub/Educational-projects/iCons/temp44040.csv")
power_df = pd.read_csv("/Users/antonioescallon23/Documents/GitHub/Educational-projects/iCons/power_curve2.csv")
print(df)

def logLaw(windSpeedR):
    zr = 9    #Reference Height i.e. buoy height (m)
    z0 = 0.0061    #Surface Roughness Factor (m)
    z=128       #Average offshore turbine hub height (m)
    windSpeed = np.log(z/z0-zr/z0)*windSpeedR
    return windSpeed

def vectorConversion(windSpeed, windDireciton):
    u = windSpeed*math.cos(windDireciton)
    v = windSpeed*math.sin(windDireciton)
    return u, v

def convertFiles(df):
    wind_list = []
    wind_vector = []
    uvector = []
    vvector = []
    for date in df[date_column]:
        wind_list.append(logLaw(df[windSpeed_column]))
        wind_vector.append(vectorConversion(df[windSpeed_column, windDirection_column]))
        u , v = vectorConversion(df[windSpeed_column, windDirection_column])
        uvector.append(u)
        vvector.append(v)

    return uvector 

def power_converte(df, power_df, date_column, power_column, wind_column_p, wind_column):
    power_list = []
    for i in range(len(df)):
        for b in range(len(power_df)):
            if(df[speed_dolumn][i] == power_df[speed_column][b]):
                power_list.append(power_df[power_column][b])

    return power_list


enercon_e126 = {
    "turbine_type": "E-126/4200",  # turbine type as in register
    "hub_height": 135,  # in m
}
e126 = WindTurbine(**enercon_e126)

print(logLaw(30))
