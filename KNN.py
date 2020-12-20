import pandas as pd
import numpy as np
from fancyimpute import KNN


def CompleteByKNN(df):
    date_list = df['Date'].astype(str).tolist()
    month_list = [int(x[5:7]) for x in date_list]
    temp_df = pd.DataFrame({"Date":month_list, "Value": df.iloc[:, 2].tolist()})
    fill_knn = KNN(k=3).fit_transform(temp_df)
    temp_df = pd.DataFrame(fill_knn)
    df.iloc[:, 2] = temp_df.iloc[:, 1]
    return df