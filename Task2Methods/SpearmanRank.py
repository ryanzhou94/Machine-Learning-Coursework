

def SpearmanRank(df):
    df2 = df.copy()
    return df2.corr(method='spearman', min_periods=1)