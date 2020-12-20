import pandas as pd
import numpy as np
from fancyimpute import KNN


def CompleteByKNN(df):
    # extract the date column as a string list
    date_list = df['Date'].astype(str).tolist()
    # extract the month value
    month_list = [int(x[5:7]) for x in date_list]
    # construct a new data frame with month list and value list
    temp_df = pd.DataFrame({"Date":month_list, "Value": df.iloc[:, 2].tolist()})
    # complete missing data by using KNN
    fill_knn = KNN(k=3).fit_transform(temp_df)
    temp_df = pd.DataFrame(fill_knn)
    # replace the original column with the new full column
    df.iloc[:, 2] = temp_df.iloc[:, 1]
    return df