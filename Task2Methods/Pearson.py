import pandas as pd


def PearsonCorr(df):
    df2 = df.copy()
    return df2.corr(method='pearson', min_periods=1)