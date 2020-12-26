import pandas as pd

# set the max row and column numbers for printing
pd.set_option('display.max_rows',1000)
pd.set_option('display.max_columns',1000)

# Open the xlsx file by using 'openpyxl'
file_path_Complete = 'China Lake Complete.xlsx'
file_path_Cleaned = 'China Lake Cleaned.xlsx'
df_Cleaned = pd.read_excel(file_path_Cleaned, engine='openpyxl')
sheets = pd.read_excel(file_path_Complete, engine='openpyxl', sheet_name=[0, 1])
df_Mean = sheets[0]
df_KNN = sheets[1]

df_Cleaned = df_Cleaned.iloc[:, 6:9]
df_Mean = df_Mean.iloc[:, 6:9]
df_KNN = df_KNN.iloc[:, 6:9]

print("Cleaned: ", df_Cleaned.std())
print("KNN: ",df_KNN.std())
print("Mean: ",df_Mean.std())