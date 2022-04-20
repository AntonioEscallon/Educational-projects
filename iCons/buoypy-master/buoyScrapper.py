import buoypy as bp
import matplotlib.pyplot as plt
import pandas as pd

buoy = 44040 #wilmington harbor
#44097
#BZBM3
#MTKN6
#NLNC3
B = bp.realtime(buoy) #wilmington harbor

def create_list(station_file, stationID_column):
    station_list = []
    for station in station_file[stationID_column]:
        station_list.append(station)
    
    return station_list


def create_df(buoy_list, date_column, function_1, function_2, **kwargs):

    for station in buoy_list:
        print(station)
        temp_file = bp.realtime(station)
        print(temp_file)
        temp_df = temp_file.txt()
        print(temp_df.index)
        temp_df = temp_df[[function_1, function_2]]
        temp_df.to_csv('station' + station + '.csv', sep='\t', encoding='utf-8')


id = 'ID'
date_column = 'index'
function_1 = 'WSPD'
function_2 = 'WDIR'

station_file = pd.read_csv('/Users/antonioescallon23/Documents/GitHub/Educational-projects/iCons/buoypy-master/Buoy Locations - Sheet1.csv')

station_list = create_list(station_file, id)
create_df(station_list, date_column, function_1, function_2)

# plotting
# fig,ax = plt.subplots(2,sharex=True)
# df.WSPD.plot(ax=ax[0])
# ax[0].set_ylabel('Wind Speed (m/s)',fontsize=14)

# df.DPD.plot(ax=ax[1])
# ax[1].set_ylabel('Dominant Period (sec)',fontsize=14)
# ax[1].set_xlabel('')
#sns.despine()