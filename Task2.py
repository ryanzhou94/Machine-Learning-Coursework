import pandas as pd
from Task2Methods.Pearson import PearsonCorr
from Task2Methods.SpearmanRank import SpearmanRank
from Task2Methods.KendallRank import KendallRank
from Task2Methods.Distance import Distance
from Task2Methods.Biweight import Biweight

# set the max row and column numbers for printing
pd.set_option('display.max_rows',1000)
pd.set_option('display.max_columns',1000)

# Open the xlsx file
file_path_Mean = 'China Lake_Mean.xlsx'
file_path_KNN = 'China Lake_KNN.xlsx'

# Open the xlsx file by using 'openpyxl'
df = pd.read_excel(file_path_KNN, engine='openpyxl')
df = df.loc[:, ['CHLA (mg/L)', 'TEMPERATURE (Centrigrade)', 'Total P (mg/L)']]

# get correlation dataframe
df_pearson_corr = PearsonCorr(df)
df_spearman_corr = SpearmanRank(df)
df_kendall_corr = KendallRank(df)
df_distance_corr = Distance(df)
df_Biweight_corr = Biweight(df)

# create a dataframe of differet methods for correlation
df_corr = pd.DataFrame({'Pearson': df_pearson_corr.iloc[:, 0],
                        'Spearman Rank' : df_spearman_corr.iloc[:, 0],
                        'Kendall Rank' : df_kendall_corr.iloc[:, 0],
                        'Distance' : df_distance_corr.iloc[:, 0],
                        'Biweight' : df_Biweight_corr.iloc[:, 0]})

# reorder the sheet
df_corr['order'] = [1, 3, 2]
df_corr = df_corr.sort_values(by='order')
df_corr.drop(columns=['order'], inplace=True)

# save excel file to local
df_corr.to_excel("China Lake_Correlation.xlsx")