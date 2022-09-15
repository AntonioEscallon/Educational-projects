from calendar import month, month_name
import pandas as pd
import pyodbc
import numpy as np
import os
import scipy.optimize
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

#initialize values to be updated for each row in dataframe and used for heuristic
curDate = ""
curHour = 0
curGridLoad = 0
curDemand = 0
curAQEW = 0
curTemperature = 0
curDayOfWeek = ""
curMonth = 0

JanDemand = 35 #Tentative average... should find out whats wrong
FebDemand  = 41.15
MarDemand = 39.83
AprDemand = 40.65
MayDemand= 40
JunDemand = 40.07
JulDemand = 41.35
AugDemand  = 41.41
SepDemand = 41.12
OctDemand = 41.48


JanSigma = 5
FebSigma = 5
MarSigma = 5
AprSigma = 5
MaySigma = 5
JunSigma = 5
JulSigma = 5
AugSigma = 5
SepSigma = 5
OctSigma = 5
NovSigma = 5
DecSigma = 5

high_hours = [6, 7, 8 , 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
low_hours = [1, 2, 3, 4, 5, 21, 22, 23, 24]

month_predicted_peak = [JanDemand,FebDemand, MarDemand, AprDemand, MayDemand, JunDemand, JulDemand, AugDemand, SepDemand, OctDemand]
month_sigma = [JanSigma,FebSigma, MarSigma, AprSigma, MaySigma, JunSigma, JulSigma, AugSigma, SepSigma, OctSigma, NovSigma, DecSigma]
month_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

timeStampColumnName = 'Date' 
dayColumnName = 'Day' 
hourColumnName = 'Hour Ending'
loadColumnName = 'Locational Marginal Price'
monthColumnName = 'Month'
yearColumnName = "Year"
averageColumnName = "Average" 
sigmaColumnName = "Sigma"

#Set boundary values to be used in heuristic
min_hour_1 = 3
min_hour_2 = 9  #tends to actually peak in the morning so look over this
max_hour = 24
#When evaluating the data in excel, the average grid load fell at around 600, and the standard deviation fell at around 47.
#600 was used as a safe starting point in our function with, since we are 100% sure no peak will be below 600. Using 600 here
#helps us avoid calling low loads peaks just because we haven't had a high load hour. 600 reduces the number of false enegatives. 
min_demand = 35

#set heuristic booleans for each of the data categories

heuristicHour = curHour <= min_hour_1 or (curHour >= min_hour_2 and curHour <= max_hour)
heuristicDemand = curGridLoad > min_demand

#set overall heuristic to evaluate data as possible peaks
heuristic = heuristicHour and heuristicDemand

'''
INFORMATION:
-----------

This function will use a heuristic to evaluate all data on Ontario and create a dataframe that only contains rows of the total data
that could potential be possible GA Peak Hours, as determined by the heuristic. 

PARAMETERS:
----------

allData_df: Dataframe
    Dataframe containing all information on Ontario--Demand, Hour, Date, AQEW, HOEP, and Temperature. 

RETURNS:
-------

hypothesisHours_df: Dataframe
    Dataframe storing the resulting rows that are possible peak Hours as determined by the heuristic. 

'''
def findTotalHours(allData_df, prediction_accuracy, month_Calc):
    #initialize hypothesis dataframe
    hypothesisHours_df = pd.DataFrame(columns=[timeStampColumnName,hourColumnName, loadColumnName])
    previous_peak = 0
    monthCount = -1
    for row in allData_df.iterrows():
        row = row[0]

        #set variables for this specific row in dataframe
        curDate = allData_df[timeStampColumnName][row]
        curHour = allData_df[hourColumnName][row]
        curGridLoad= allData_df[loadColumnName][row]
        curMonth = allData_df[monthColumnName][row]

        #ensure all data types are proper for comparison
        curDate = str(curDate)
        curHour = int(curHour)
        curGridLoad = float(curGridLoad)
        curMonth = int(curMonth)

        #set heuristic booleans for each of the data categories
        heuristicHour = curHour <= min_hour_1 or (curHour >= min_hour_2 and curHour <= max_hour)
        
        if(curMonth != monthCount):
            monthCount = curMonth
            previous_peak = month_Calc[averageColumnName][curMonth - 1]

        if (curGridLoad > previous_peak):
            previous_peak = curGridLoad

        if(curGridLoad + 2.5*month_Calc[sigmaColumnName][curMonth - 1]*prediction_accuracy > previous_peak):
            heuristicDemand = True
        else:
            heuristicDemand = False
            
        #set overall heuristic to evaluate data as possible peaks
        heuristic = heuristicHour and heuristicDemand
        #if the heuristic is true for this row, then this row is a potential peak hour and will be added to hypothesis df.
        if heuristic:
            hypothesisHours_df = hypothesisHours_df.append({timeStampColumnName :curDate, monthColumnName: curMonth, hourColumnName :curHour, 
            dayColumnName: curDayOfWeek, loadColumnName: curGridLoad}, ignore_index=True)
    return hypothesisHours_df

#Convertint to the same format. Hopefully it will be fitting into SQL
def convertSQLFormat(sql_df):
    
    formatted_df = sql_df
    formatted_df[timeStampColumnName]= formatted_df[timeStampColumnName].astype(str)
    formatted_df[yearColumnName] =  formatted_df[timeStampColumnName].str.slice(6, 10)
    formatted_df[monthColumnName] =  formatted_df[timeStampColumnName].str.slice(0, 2)
    formatted_df[dayColumnName] =  formatted_df[timeStampColumnName].str.slice(3, 5)
    formatted_df[hourColumnName] =  formatted_df[hourColumnName]

    return formatted_df


#Basic training of data rleying on historic average and stdev
def train_to_find_data(data, month_list, month_column_name):

    math_df = pd.DataFrame(columns=[monthColumnName, averageColumnName, sigmaColumnName])
    list_month = []
    math_df[monthColumnName] = month_list
    for monthNumber in month_list:
        #Separating each month into a dicitonary and getting the stdv
        for i in range(len(data)):
            if monthNumber == int(data[monthColumnName][i]):
                list_month.append(data[loadColumnName][i])
        math_df[averageColumnName][monthNumber - 1] = sum(list_month) / len(list_month)
        math_df[sigmaColumnName][monthNumber - 1] = np.std(list_month)
        list_month = []

    return math_df

#Creating a really bad forecast
def how_high(df, date_column, high_hours, month_Calc, lmp_column, hour_column, repetitions):

    new_lmp = [0]
    count = 1
    for i in range(1, len(df[date_column])):
        curMonth = int(df[monthColumnName][i])
        if df[date_column][i] == df[date_column][i -1] or count != repetitions:
            if np.isin(df[hour_column][i], high_hours):
                new_lmp.append(df[lmp_column][2] + 0.05*month_Calc[sigmaColumnName][curMonth - 1]*prediction_accuracy*df[hour_column][i])
            else:
                new_lmp.append(df[lmp_column][0] - 0.05*month_Calc[sigmaColumnName][curMonth - 1]*prediction_accuracy*df[hour_column][i])
        else:
            break
        count = count+1
    print(count)
    return new_lmp

    # for row in data.iterrows():
    #     row = row[0]
    #     #set variables for this specific row in dataframe
    #     curDate = data[timeStampColumnName][row]
    #     curHour = data[hourColumnName][row]
    #     curGridLoad= data[loadColumnName][row]
    #     curMonth = data[monthColumnName][row]

    #     #ensure all data types are proper for comparison
    #     curDate = str(curDate)
    #     curHour = int(curHour)
    #     curGridLoad = float(curGridLoad)
    #     curMonth = int(curMonth)

lmp_column = 'Locational Marginal Price'
hour_column = 'Hour Ending'
date_column = 'Date'




    
prediction_accuracy = 0.95
df = pd.read_csv('/Users/antonioescallon23/Documents/GitHub/Educational-projects/data/LMP_data/station4000.csv', sep='\t')
old_df = convertSQLFormat(df)
month_Calc = train_to_find_data(old_df, month_list, monthColumnName)
repetitions = len(old_df) + 2
print(repetitions)
new_list = how_high(old_df, date_column, high_hours, month_Calc, lmp_column, hour_column, repetitions)
print(len(new_list))
print(len(old_df))
old_df["new_calc"] = new_list
old_df.to_csv("new_calc.csv")
# new_df = findTotalHours(old_df, prediction_accuracy, new_data_df)
# print(new_df)