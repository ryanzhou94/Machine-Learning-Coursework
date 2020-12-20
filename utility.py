import pandas as pd
import numpy as np

def clean(sheet):
    # Change column name
    target_name = sheet.columns.values[6]
    if target_name == 'TEMPERATURE（Centrigrade）':
        sheet.rename(columns={'DEPTH':'Depth'}, inplace=True)

    # Processs sheet:
    # We will only process the date, depth, target item (CHLA, TEMPERATUR and Total P),
    # therefor, we drop irrelevant items, which are MIDAS, LAKE, Town(s) and STATION
    # With the reduced amount of data, the program will process data much faster
    df = sheet.loc[:, ['Date', 'Depth', target_name]]

    # Select one depth by dropping irrelevant depths
    df.drop(df[df.Depth != 7].index, inplace=True)
    df = df.sort_values(by='Date')
    df.reset_index(drop=True, inplace=True)

    # Select valid date
    #   a. between 1998-5-1 to 2013-10-31
    #   b. exclude 2004
    #   c. month between 5 to 10
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


    # Calculate mean value for each month
    # if dates have same year and month, there target value will be added up
    # and a new piece of data will be created
    # Get the first data
    Year = df.loc[0, 'Date'].year
    Month = df.loc[0, 'Date'].month
    Target = df.loc[0, target_name]
    Total = 1
    new_target_list = []
    # if the first a few months are missing,
    # add NaN to the list
    for i in range (Month - 5):
        new_target_list.append(-1)
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
                        new_target_list.append(-1)
            else:
                # different year
                if (month_delta + 5) != 0:
                    for i in range(month_delta + 5):
                        new_target_list.append(-1)
            # new piece of data
            Year = year
            Month = month
            Target = target
            Total = 1
        if index == len(df) - 1:
            mean_value = round(((Target * 100) / 100.0) / Total, 5)
            new_target_list.append(mean_value)

    # Get full year-month-day except 2004 since there is no useful data for 2004
    empty_date_list = []
    for year in range(1998, 2014):
        if year == 2004:
            continue
        for month in range(5, 11):
            empty_date_list.append(pd.to_datetime(str(year) + '-' + str(month) + '-1'))

    # print(len(empty_date_list))
    # print(len(new_target_list))

    # create a new DataFrame
    new_sheet = pd.DataFrame({'Date': empty_date_list, 'Depth': 7, target_name: new_target_list})

    return new_sheet