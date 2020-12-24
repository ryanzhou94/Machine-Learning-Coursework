import pandas as pd

# set the max row and column numbers for printing
pd.set_option('display.max_rows',1000)
pd.set_option('display.max_columns',1000)

# Open the xlsx file by using 'openpyxl'
file_path_Cleaned = 'China Lake_cleaned.xlsx'
file_path_Mean = 'China Lake_Mean.xlsx'
file_path_KNN = 'China Lake_KNN.xlsx'
df_Cleaned = pd.read_excel(file_path_Cleaned, engine='openpyxl')
df_Mean = pd.read_excel(file_path_Mean, engine='openpyxl')
df_KNN = pd.read_excel(file_path_KNN, engine='openpyxl')

df_Cleaned = df_Cleaned.iloc[:, 6:9]
df_Mean = df_Mean.iloc[:, 6:9]
df_KNN = df_KNN.iloc[:, 6:9]

print("Cleaned: ", df_Cleaned.std())
print("KNN: ",df_KNN.std())
print("Mean: ",df_Mean.std())