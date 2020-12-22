import pandas as pd
import numpy as np

# clean sheets: 1. drop irrelevant date, year and depth
#               2. calculate the mean value for each month from May to October
#               3. add 'NaN' to missing month
def clean(df):
    # Change column name
    df = PreprocessColumnNames(df)

    # Process sheet:
    # We will only process the date, depth, target item (CHLA, TEMPERATUR and Total P),
    # therefor, we drop irrelevant items, which are MIDAS, LAKE, Town(s) and STATION
    # With the reduced amount of data, the program will process data much faster
    # The dropped columns will be added to the final sheet
    df = df.loc[:, ['Date', 'Depth', df.columns.values[6]]]

    # Select one appropriate depth (7) by dropping irrelevant depths
    df = selectValidDepth(df)

    # Select valid date
    #   a. between 1998-5-1 to 2013-10-31
    #   b. exclude 2004 (there is no valid data for 'CHLA' in 2004)
    #   c. between May to October (5-10)
    df = selectValidDate(df)

    # Get full year-month-day except 2004 since there is no useful data for 2004
    empty_date_list = getFullDateList()

    # Calculate mean value for each month
    # if two dates have the same year and month, their target values will be added up
    # and a new piece of data will be created
    # if there is no data for a month, a 'NaN' will be added
    new_target_list = getMeanValueList(df)

    # create a new DataFrame and return it
    return pd.DataFrame({'Date': empty_date_list, 'Depth': 7, df.columns.values[2]: new_target_list})


# Change column name:
#   if the target column name is 'DEPTH', then change it to 'Depth'
def PreprocessColumnNames(df):
    target_name = df.columns.values[6]
    if target_name == 'TEMPERATURE（Centrigrade）':
        df.rename(columns={'DEPTH':'Depth'}, inplace=True)
    return df

# Select one appropriate depth (7) by dropping irrelevant depths
def selectValidDepth(df):
    df.drop(df[df.Depth != 7].index, inplace=True)
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

# Calculate mean value for each month
# if two dates have the same year and month, their target values will be added up
# and a new piece of data will be created
# if there is no data for a month, a 'NaN' will be added
def getMeanValueList(df):
    Year = df.loc[0, 'Date'].year
    Month = df.loc[0, 'Date'].month
    Target = df.iloc[0, 2]
    Total = 1
    new_target_list = []
    # if the first a few months are missing,
    # add NaN to the list
    for i in range(Month - 5):
        new_target_list.append(np.nan)
    # Iterate the dataframe
    for tup in df.itertuples():
        index = tup[0]
        year = tup[1].year
        month = tup[1].month
        target = tup[3]

        # if it is the first data, continue
        if index == 0:
            continue

        # if two piece of data have same year and month
        if (Year == year) & (Month == month):
            Target += target
            Total += 1
            # if the current data is the last piece of data, calculate the mean value and append it to the list
        else:
            # calculate the previous mean value first
            mean_value = round(((Target * 100) / 100.0) / Total, 5)
            new_target_list.append(mean_value)

            # Add empty data
            month_delta = month - Month
            if Year == year:
                if month_delta != 1:
                    for i in range(month_delta - 1):
                        new_target_list.append(np.nan)
            else:
                # different year
                if (month_delta + 5) != 0:
                    for i in range(month_delta + 5):
                        new_target_list.append(np.nan)
            # new piece of data
            Year = year
            Month = month
            Target = target
            Total = 1
        if index == len(df) - 1:
            mean_value = round(((Target * 100) / 100.0) / Total, 5)
            new_target_list.append(mean_value)
    return new_target_list

# Get full year-month-day except 2004 since there is no useful data for 2004
def getFullDateList():
    empty_date_list = []
    for year in range(1998, 2014):
        if year == 2004:
            continue
        for month in range(5, 11):
            empty_date_list.append(pd.to_datetime(str(year) + '-' + str(month) + '-1'))
    return empty_date_list