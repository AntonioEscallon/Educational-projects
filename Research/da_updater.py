# A common func
# def back_fill_fuel_mix(start, end):
#    day = start
#    while (day <= end):
#        update_fuel_mix(day)
#        day += datetime.timedelta(days=1)tion that allows for generic realtime or manual scraping of data

import datetime
import time
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import pyodbc
import sqlalchemy
import pytz

import os,sys
# Allows upper level imports
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from webscraper.scraper_common import *
import server_info
from Carbon_Accounting.daily_csv_data_reader import convert_to_utc

import os,sys
# Allows upper level imports
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from day_ahead_opt.sql_link import create_SQL_engine
from common_tools import sql_last_value, newest_released, upload_unique

# iso_urls = {'NYISO': 'http://mis.nyiso.com/public/csv/damlbmp/' + year + month + day + 'damlbmp_zone.csv'} 
# iso_urls = {'ISONE': 'https://www.iso-ne.com/static-transform/csv/histRpts/da-lmp/WW_DALMP_ISO_' + year + month + day + 'csv'}

utc = pytz.utc

lmp_table = "dalmp"

lmp_date_format = "%m/%d/%Y %H:%M"

hours_to_convert_to_tz = 4

# Takes a the last entry of a sql database and checks it with a given date to
# See if that date is a new entry in the database
def check_if_new(sql_newest, csv_newest, tz):
    # Converts last entry to local time for comparison
    sql_newest = utc.localize(sql_newest).astimezone(tz).replace(tzinfo=None)
    csv_date = datetime.datetime(csv_newest.year, csv_newest.month, csv_newest.day, csv_newest.hour, csv_newest.minute)
    sql_date = datetime.datetime(sql_newest.year, sql_newest.month, sql_newest.day, sql_newest.hour, sql_newest.minute)
    
    log(INFO, "webscrapper", "check_if_new", "", variables = {"SQL" : sql_date})
    log(INFO, "webscrapper", "check_if_new", "", variables = {"CSV" : csv_date})
    
    # if csv date is newer than we should update
    return csv_date > sql_date

   
# Returns True if the there is a value in the csv that is not in the SQL database
# Inputs: table -> the table to examine for lastest entry
#         timestamp_index -> index of the column which stores the timestamp
#         to_csv -> Function that returns a csv file given a date
#         date_format -> format of the date
#         timestamp_name -> name of the timestamp column
def is_new(table, timestamp_index, to_csv, date_format, 
           timestamp_name = "Timestamp", tz = tz, 
           date = datetime.datetime.now(), return_downloaded = False,
           database = server_info.database, iso = ''):
    csv_output = newest_released(to_csv,date_format, timestamp_name, date = date)
    # If an empty df is returned by the csv (e.g. no data exists to download) then
    # we can short circut the rest of the work
    
    if (not (csv_output)):
        return False, None
    else:
        # Otherwise expect that we were given a standard output
        csv_newest, csv_df = csv_output 
    sql_newest = sql_last_value(database, table, timestamp_index, iso = iso)
 
       
    if (return_downloaded):
        return check_if_new(sql_newest, csv_newest, tz), csv_df
    return check_if_new(sql_newest, csv_newest, tz)

def update_day_ahead(table, 
                     to_csv, 
                     date, 
                     new_names, 
                     to_save, 
                     date_format, 
                     primary_keys, 
                     additional_transform = None,
                     iso = 'NYISO', 
                     tz = pytz.timezone('US/Eastern'),
                     downloaded_data = pd.DataFrame(),
                     database = server_info.database):
    '''
    Check Day Ahead data for updates, scrape new data, and push to sql


    Inputs:
        table  = the table to update
        to_csv = function that  takes the date and produces a url from which to get the csv
        date = the time of the new date to get (e.g. today) 
        new_names = dict containing new names for columns
        to_save = columns to save into the sql
        date_format = format of date string
        primary_keys = 
        additional_transform = a function that takes a df and performs the necessary transforms, only used with some inputs
    Output:
        updates the given table if there is a new value

    '''
    # Initialize Pandas dataframe to store LMP data
    df = pd.DataFrame()

    # Initialize updated variable
    updated = False

    # Initialize counter

    # Continue while day ahead data has not been updated
    # and while counter has not hit maximum time allowed
    # Attempt to connect to day-ahead schedule
    # if CSV file not yet published skips to exception
    # try:
    # Read CSV file into pandas dataframe
    if (not downloaded_data.equals(pd.DataFrame())):
        df = downloaded_data
    else:
        df = to_csv(date) 

    if (pd.DataFrame().equals(df)):
        return False

    # Rename columns to match with SQL schema
    df.rename(columns=new_names, inplace=True)
    
    # Deletes columns that are not being saved
    for column in df.columns.values:
        if not column in to_save:
            del df[column]


    # Converts the datatimes of the downloaded csv to UTC
    df = convert_to_utc(df, date_format, len(df.columns.unique()))

    df['Timestamp'] = pd.DatetimeIndex(pd.to_datetime(df['Timestamp'])).tz_localize(None)
    
    # Create and fill ISO column
    df['ISO'] = iso
    
    if (additional_transform != None):
        df = additional_transform(df)
   
    return upload_unique(table, df, primary_keys, database = database)

# Updates a SQL database using a wide, predefined range
def update_all_type(update_day_ahead_specific):
    end_date = datetime.datetime.strptime('2019-03-11', '%Y-%m-%d')
    start_date = datetime.datetime.strptime('2018-03-10', '%Y-%m-%d')
    date = start_date
    while(date <= end_date):
       update_day_ahead_specific(date)
       date += datetime.timedelta(days=1)

def lmp_vs_schedule():
    schedule_table = 'dbo.schedule'
    schedule_timestamp_index = 1
    to_csv = lmp_updater
    return is_new('dbo.schedule', timestamp_index, to_csv, date_format, timestamp_name = "Timestamp")