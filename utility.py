import pandas as pd
import numpy as np
import math

# Drop irrelevant data and merge 3 tables
# After the merge, month mean value will be calculated
# A cleaned and merged table will be returned
def merge3Tables(df1, df2, df3):
    # drop irrelevant data
    df1 = dropIrrelevant(df1)
    df2 = dropIrrelevant(df2)
    df3 = dropIrrelevant(df3)

    # merge 3 tables
    result = pd.merge(df1, df2, how='outer', on=['Date', 'Depth'])
    result = pd.merge(result, df3, how='outer', on=['Date', 'Depth'])
    result.sort_values(by='Date', inplace=True)
    result.reset_index(drop=True, inplace=True)

    # calculate month mean values and return the table
    result = getMeanValueSheet(result)

    # create a full dataframe
    df = pd.DataFrame({"MIDAS": 5448, "Lake": "China Lake", "Town": "China, Vassalboro", "Station": 1,
                       "Date": result['Date'].dt.date, "Depth": 7, "CHLA (mg/L)": result.iloc[:, 1],
                       "TEMPERATURE (Centrigrade)": result.iloc[:, 2],
                       "Total P (mg/L)": result.iloc[:, 3]})
    return df


def getMeanValueSheet(df):
    # create a new dataframe for function output
    df_new = pd.DataFrame({"Date":[], "CHLA (mg/L)":[], "TEMPERATURE (Centrigrade)":[], "Total P (mg/L)":[]})
    for year in range(1998, 2014):
        if year == 2004:
            # exclude year 2004 because there is no data for CHLA in 2004
            continue
        for month in range(5, 11):
            # get data in year-month
            temp_df = getYearMonthData(df, year, month)
            if checkEmpty(temp_df):
                # if all three values are NaN, add three NaN to the new dateframe
                temp_row = pd.DataFrame({"Date":constructDate(year, month), "CHLA (mg/L)": np.nan, "TEMPERATURE (Centrigrade)":np.nan, "Total P (mg/L)":np.nan}, index=[1])
                df_new = df_new.append(temp_row, ignore_index=True)
            elif checkComplete(temp_df):
                # if there are three values are not NaN, only calculate each mean value to that month and drop incomplete data
                # get complete data
                df_complete = getComplete(temp_df)
                # get mean value for each variable
                chla_mean = calculateMean(df_complete, 0)
                temperature_mean = calculateMean(df_complete, 1)
                totalp_mean = calculateMean(df_complete, 2)
                # add mean values to the new dataframe
                temp_row = pd.DataFrame({"Date":constructDate(year, month), "CHLA (mg/L)": chla_mean, "TEMPERATURE (Centrigrade)":temperature_mean, "Total P (mg/L)":totalp_mean}, index=[1])
                df_new = df_new.append(temp_row, ignore_index=True)
            else:
                # if all pieces of data are incomplete, calculate their mean values
                chla_mean = calculateMean(temp_df, 2)
                temperature_mean = calculateMean(temp_df, 3)
                totalp_mean = calculateMean(temp_df, 4)
                # add mean values to the new dataframe
                temp_row = pd.DataFrame({"Date": constructDate(year, month), "CHLA (mg/L)": chla_mean,
                                         "TEMPERATURE (Centrigrade)": temperature_mean, "Total P (mg/L)": totalp_mean},
                                        index=[1])
                df_new = df_new.append(temp_row, ignore_index=True)
    return df_new


# Process column names: 'DEPTH' -> 'Depth'; 'STATION' -> 'Station'
# Select valid depth: 7
# Select valid station: 1
# Select valid data: May to October from 1998 to 2013, excluding 2004
def dropIrrelevant(df):
    df = PreprocessColumnNames(df)
    df = selectValidDepth(df)
    df = selectValidStation(df)
    df = selectValidDate(df)
    df = df.loc[:, ['Date', 'Depth', df.columns.values[6]]]
    return df


# Change column name:
#   if the target column name is 'DEPTH', then change it to 'Depth'
#   if the target column name is 'STATION', then change it to 'Station'
def PreprocessColumnNames(df):
    if df.columns.values[6] == 'TEMPERATURE（Centrigrade）':
        df.rename(columns={'DEPTH':'Depth'}, inplace=True)
    if df.columns.values[3] == 'STATION':
        df.rename(columns={'STATION':'Station'}, inplace=True)
    return df


# Select one appropriate depth (7) by dropping irrelevant depths
def selectValidDepth(df):
    df.drop(df[df.Depth != 7].index, inplace=True)
    df = df.sort_values(by='Date')
    df.reset_index(drop=True, inplace=True)
    return df


# Select one appropriate station (1) by dropping irrelevant stations
def selectValidStation(df):
    df.drop(df[df.Station != 1].index, inplace=True)
    df = df.sort_values(by='Date')
    df.reset_index(drop=True, inplace=True)
    return df


# Select valid date
#   a. between 1998-5-1 to 2013-10-31
#   b. exclude 2004 (there is no valid data for 'CHLA' in 2004)
#   c. between May to October (5-10)
def selectValidDate(df):
    start = pd.to_datetime('1998-5-1')
    end = pd.to_datetime('2013-10-31')
    valid_month = [5, 6, 7, 8, 9, 10]
    for index, date in enumerate(df.Date):
        if (date < start) | (date > end):
            df.drop(index, inplace=True)
            continue
        if date.month not in valid_month:
            df.drop(index, inplace=True)
            continue
        if date.year == 2004:
            df.drop(index, inplace=True)
            continue
    df.reset_index(drop=True, inplace=True)
    return df


# Get data in year-month
def getYearMonthData(df, year, month):
    df2 = df.copy()
    for index, date in enumerate(df2.Date):
        # only leave the data that has the same year and month with 'year' and 'month', and drop the rest
        if (date.year != year) | (date.month != month):
            df2.drop(index, inplace=True)
    df2.reset_index(drop=True, inplace=True)
    return df2


# Construct a '<class 'pandas._libs.tslibs.timestamps.Timestamp'>'
def constructDate(year, month):
    date_str = str(year) + '-' + str(month)
    return pd.to_datetime(date_str)


# Check if there is any complete data in the dataframe
def checkComplete(df):
    isComplete = False
    for i in range(len(df.index)):
        # if there are three non-Nan value on the same day, isComplete = True and return it
        if (math.isnan(df.iloc[i, 2]) == False) & (math.isnan(df.iloc[i, 3]) == False) & (math.isnan(df.iloc[i, 4]) == False):
            isComplete = True
            break
    return isComplete


# Return complete data
def getComplete(df):
    chla_list = []
    temperature_list = []
    totalp_list =[]
    for i in range(len(df.index)):
        if (math.isnan(df.iloc[i, 2]) == False) & (math.isnan(df.iloc[i, 3]) == False) & (math.isnan(df.iloc[i, 4]) == False):
            chla_list.append(df.iloc[i, 2])
            temperature_list.append(df.iloc[i, 3])
            totalp_list.append(df.iloc[i, 4])
    df_complete = pd.DataFrame({"CHLA (mg/L)":chla_list, "TEMPERATURE (Centrigrade)":temperature_list, "Total P (mg/L)":totalp_list})
    return df_complete


# Check if the dataframe is empty
def checkEmpty(df):
    return len(df.index) == 0


# Calculate mean value for a row
def calculateMean(df, row_number):
    list = df.iloc[:, row_number].tolist()
    total = 0
    count = 0
    for i in list:
        if math.isnan(i) == False:
            total += i
            count += 1
    if count == 0:
        return np.nan
    else:
        return total / count