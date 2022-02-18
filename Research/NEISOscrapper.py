import os,sys
# Allows upper level imports
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from webscraper.da_updater import update_day_ahead, is_new
from common_tools import sql_last_value, newest_released
from Carbon_Accounting.daily_csv_data_reader import read_file_from_s3
import datetime
from logs.log_medley import *
import server_info
import pandas as pd
from webscraper.lmp_scraper import lmp_vs_schedule


# This file allows for the scrapping LMP data

iso = 'ISONE'

lmp_table = "dalmp"

lmp_date_format = "%m/%d/%Y %H:%M"

url = 'https://www.iso-ne.com/static-transform/csv/histRpts/da-lmp/WW_DALMP_ISO_'

options = {'.H.INTERNAL_HUB', '.Z.MAINE',
'.Z.NEWHAMPSHIRE',
'.Z.VERMONT',
'.Z.CONNECTICUT',
'.Z.RHODEISLAND',
'.Z.SEMASS',
'.Z.WCMASS',
'.Z.NEMASSBOST'}

expected_time = 17

# Method to access lmp data from either saved sources or the web
# Inputs:
#  - date: the date passed in should be configured in such a way as to ensure proper operation
#   TODO: This is a very weird method and should at the least be better documented (Chris, 3/31/2021)
def lmp_to_csv_ne(date):
    current_time = pd.to_datetime('now')
    current_hour = current_time.hour
    if(current_hour > expected_time):
        current_day = datetime.datetime.now() + datetime.timedelta(days = 1)
        c_day = current_day.day
        c_month = current_day.month
    else:
        current_day = datetime.datetime.now()
        c_day = current_day.day
        c_month = current_day.month
    try:
        name = url + str(date.year) + str(date.month).zfill(2) + str(date.day).zfill(2) + '.csv'
        
        log(INFO, "webscrapper", "lmp_to_csv_ne", "Getting DALMP CSV from HTML",
            variables = {"HTML" : name})
        print(name)
        
        # Skipping rows is required due to the difference in format of the csv. Footer also needs to be skipped due to the same reason. 
        data = pd.read_csv(name, skiprows=[0,1,2,3,5], skipfooter=1, engine='python')
        
        #Added this line in case a Timestamp column is needed beforehand. 
        data['Time Stamp'] = data['Date'].astype(str) + ' ' + (data['Hour Ending'].astype(int) - 1).astype(str) + ':00'

        # Dropping all nodes besides the hub nodes
        filtered_data = data[data['Location Name'].isin(options)]
        
        return filtered_data
    except Exception as e:
        if (date.day == c_day and date.month == c_month): 
            log(FAILURE, "webscrapper", "lmp_to_csv_ne", "LMP to CSV Failed",
                variables = {"Exception" : e})
            return pd.DataFrame()
        log(WARNING, "webscrapper", "lmp_to_csv_ne", "Getting DALMP CSV from S3")
        return pd.read_csv(read_file_from_s3("raw/isone/DALMP/WW_DALMP_ISO_" + str(date.year) + "/" + str(date.year)
                                             + str(date.month).zfill(2) + "01_csv/" + str(date.year) 
                                             + str(date.month).zfill(2) + str(date.day).zfill(2) + ".csv"))

# Call update day ahead (generic function) with appropriate paramaters
def update_dalmp_ne(database, date = datetime.datetime.now()):
    new_names = {'Time Stamp': 'Timestamp', 'Date' : 'Date', 'Hour Ending': 'Hour', 'Location ID': 'ID', 'Location Name':'Node', 'Location Type':'Location_Type', 'Locational Marginal Price': 'LMP', 'Energy Component' : 'EC', 'Congestion Component': 'MCC', 'Marginal Loss Component': 'MLC'}
    
    to_save = ['Timestamp', 'Node', 'MLC', 'MCC', 'LMP']

    # I beleive I have understood why this is not necessarily a problem.  
    primary_keys = ['Timestamp', 'Node']

    return update_day_ahead(lmp_table, lmp_to_csv_ne, date, new_names, to_save, lmp_date_format, primary_keys, iso = iso, database = database)

# Call update lmp data if there is new data
def realtime_dalmp_ne(database, date = datetime.datetime.now()):

    if (is_new(lmp_table, timestamp_index=2, timestamp_name = 'Time Stamp', to_csv=lmp_to_csv_ne,
               date_format = lmp_date_format, date = date, database = database, iso = iso)):
        update_dalmp_ne(database, date)

# Backfill lmp data 
def back_fill_lmp(start, end):
    day = start
    while (day <= end):
        print ("LMP Day: " + str(day))
        update_dalmp_ne(day)
        day += datetime.timedelta(days=1)

#start = datetime.datetime.strptime('2021-07-22', '%Y-%m-%d')
#end = datetime.datetime.strptime('2021-07-23', '%Y-%m-%d')

#back_fill_lmp(start, end)