import pandas as pd
from Task2Methods.Pearson import PearsonCorr
from Task2Methods.SpearmanRank import SpearmanRank
from Task2Methods.KendallRank import KendallRank
from Task2Methods.Distance import Distance
from Task2Methods.Biweight import Biweight

pd.set_option('display.max_rows',1000)
pd.set_option('display.max_columns',1000)

# Open the xlsx file
file_path_Mean = 'China Lake_Mean.xlsx'
file_path_KNN = 'China Lake_KNN.xlsx'

# Open the xlsx file by using 'openpyxl'
df = pd.read_excel(file_path_KNN, engine='openpyxl')
df = df.loc[:, ['CHLA (mg/L)', 'TEMPERATURE (Centrigrade)', 'Total P (mg/L)']]

# df_pearson_corr = PearsonCorr(df)
# df_spearman_corr = SpearmanRank(df)
# df_kendall_corr = KendallRank(df)
# df_distance_corr = Distance(df)
df_Biweight_corr = Biweight(df)

# print("Pearson: ", df_pearson_corr)
# print("Spearman Rank: ", df_spearman_corr)
# print("Kendall Rank: ", df_kendall_corr)
# print("Distance: ", df_distance_corr)
print("Biweight: ", df_Biweight_corr)