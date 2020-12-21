import pandas as pd
from fancyimpute import KNN


def CompleteByKNN(df):
    df2 = df.copy()
    # extract the date column as a string list
    date_list = df2['Date'].astype(str).tolist()

    # extract the month value
    month_list = [int(x[5:7]) for x in date_list]

    # construct a new data frame with month list and value list
    temp_df = pd.DataFrame({"Date":month_list, "Value": df2.iloc[:, 2].tolist()})

    # complete missing data by using KNN
    fill_knn = KNN(k=3).fit_transform(temp_df)
    temp_df = pd.DataFrame(fill_knn)

    # replace the original column with the new full column
    df2.iloc[:, 2] = temp_df.iloc[:, 1]

    df2 = pd.DataFrame({"MIDAS": 5548, "Lake": "China Lake", "Town": "China, Vassalboro", "Station": 1,
                       "Date": df2['Date'], "Depth": 7, df2.columns.values[2]: df2.iloc[:, 2]})

    return df2