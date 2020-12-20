import pandas as pd
import numpy as np

def CompleteByMean(df):
    # Go through the whole df and find missing month
    new_target_list = []
    for tup in df.itertuples():
        date = constructDate(tup[1].year, tup[1].month)
        value = getMonthValue(df, date)
        # new_target_list.append(getMonthValue(df, date))
        df.iloc[tup[0], 2] = value


def getMonthValue(df, date):
    result = np.nan
    # print(date)
    if df[df['Date'] == date].iloc[0, 2] != -1:
        # the result is not NaN, simply return the result
        result = df[df['Date'] == date].iloc[0, 2]
    else:
        # the result is -1(empty)
        if date.month == 5:
            # if it is May, use June and July
            post1 = getMonthValue(df, constructDate(date.year, 6))
            post2 = getMonthValue(df, constructDate(date.year, 7))
            result = post1 * 2 - post2
        elif date.month == 10:
            # if it is October, use September and August
            pre1 = getMonthValue(df, constructDate(date.year, 9))
            pre2 = getMonthValue(df, constructDate(date.year, 8))
            result = pre1 * 2 - pre2
        else:
            # use previous month and post month
            pre_date = constructDate(date.year, date.month-1)
            post_date = constructDate(date.year, date.month+1)
            if (df[df['Date'] == pre_date].iloc[0, 2] == -1):
                # if the previous month is -1(empty), use two post months
                post1 = getMonthValue(df, constructDate(date.year, date.month+1))
                post2 = getMonthValue(df, constructDate(date.year, date.month+2))
                result = post1 * 2 - post2
            elif (df[df['Date'] == post_date].iloc[0, 2] == -1):
                # if the post month is -1(empty), use two previous months
                pre1 = getMonthValue(df, constructDate(date.year, date.month-1))
                pre2 = getMonthValue(df, constructDate(date.year, date.month-2))
                result = pre1 * 2 - pre2
            else:
                pre = getMonthValue(df, pre_date)
                post = getMonthValue(df, post_date)
                result = (pre + post) / 2
    if result < 0:
        # set negative values to 0
        result = 0
    return result


# Construct a '<class 'pandas._libs.tslibs.timestamps.Timestamp'>'
def constructDate(year, month):
    date_str = str(year) + '-' + str(month)
    return pd.to_datetime(date_str)

