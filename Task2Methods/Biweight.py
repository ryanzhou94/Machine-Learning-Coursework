from astropy.stats import biweight_midcorrelation
import pandas as pd

def Biweight(df):
    # 0, 1
    cor_01 = biweight_midcorrelation(df.iloc[:, 0], df.iloc[:, 1])
    cor_10 = biweight_midcorrelation(df.iloc[:, 1], df.iloc[:, 0])

    # 1, 2
    cor_12 = biweight_midcorrelation(df.iloc[:, 1], df.iloc[:, 2])
    cor_21 = biweight_midcorrelation(df.iloc[:, 2], df.iloc[:, 1])

    # 0, 2
    cor_02 = biweight_midcorrelation(df.iloc[:, 0], df.iloc[:, 2])
    cor_20 = biweight_midcorrelation(df.iloc[:, 2], df.iloc[:, 0])

    # 00, 11, 22
    cor_00 = biweight_midcorrelation(df.iloc[:, 0], df.iloc[:, 0])
    cor_11 = biweight_midcorrelation(df.iloc[:, 1], df.iloc[:, 1])
    cor_22 = biweight_midcorrelation(df.iloc[:, 2], df.iloc[:, 2])

    cor_0 = [cor_00, cor_10, cor_20]
    cor_1 = [cor_01, cor_11, cor_21]
    cor_2 = [cor_02, cor_12, cor_22]

    df_corr = pd.DataFrame(columns=df.columns.values, index=df.columns.values)

    df_corr.iloc[:, 0] = cor_0
    df_corr.iloc[:, 1] = cor_1
    df_corr.iloc[:, 2] = cor_2

    return df_corr