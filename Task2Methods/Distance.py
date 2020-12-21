from scipy.spatial.distance import pdist, squareform
import numpy as np
import pandas as pd


def Distance(df):
    # 0, 1
    cor_01 = distcorr(df.iloc[:, 0], df.iloc[:, 1])
    cor_10 = distcorr(df.iloc[:, 1], df.iloc[:, 0])

    # 1, 2
    cor_12 = distcorr(df.iloc[:, 1], df.iloc[:, 2])
    cor_21 = distcorr(df.iloc[:, 2], df.iloc[:, 1])

    # 0, 2
    cor_02 = distcorr(df.iloc[:, 0], df.iloc[:, 2])
    cor_20 = distcorr(df.iloc[:, 2], df.iloc[:, 0])

    # 00, 11, 22
    cor_00 = distcorr(df.iloc[:, 0], df.iloc[:, 0])
    cor_11 = distcorr(df.iloc[:, 1], df.iloc[:, 1])
    cor_22 = distcorr(df.iloc[:, 2], df.iloc[:, 2])

    cor_0 = [cor_00, cor_10, cor_20]
    cor_1 = [cor_01, cor_11, cor_21]
    cor_2 = [cor_02, cor_12, cor_22]

    df_corr = pd.DataFrame(columns=df.columns.values, index=df.columns.values)

    df_corr.iloc[:, 0] = cor_0
    df_corr.iloc[:, 1] = cor_1
    df_corr.iloc[:, 2] = cor_2

    return df_corr



def distcorr(X, Y):
    X = np.atleast_1d(X)
    Y = np.atleast_1d(Y)
    if np.prod(X.shape) == len(X):
        X = X[:, None]
    if np.prod(Y.shape) == len(Y):
        Y = Y[:, None]
    X = np.atleast_2d(X)
    Y = np.atleast_2d(Y)
    n = X.shape[0]
    if Y.shape[0] != X.shape[0]:
        raise ValueError('Number of samples must match')
    a = squareform(pdist(X))
    b = squareform(pdist(Y))
    A = a - a.mean(axis=0)[None, :] - a.mean(axis=1)[:, None] + a.mean()
    B = b - b.mean(axis=0)[None, :] - b.mean(axis=1)[:, None] + b.mean()

    dcov2_xy = (A * B).sum() / float(n * n)
    dcov2_xx = (A * A).sum() / float(n * n)
    dcov2_yy = (B * B).sum() / float(n * n)
    dcor = np.sqrt(dcov2_xy) / np.sqrt(np.sqrt(dcov2_xx) * np.sqrt(dcov2_yy))
    return dcor