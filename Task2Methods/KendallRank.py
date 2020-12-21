

def KendallRank(df):
    df2 = df.copy()
    return df2.corr(method='kendall', min_periods=1)