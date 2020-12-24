import pandas as pd
from utility import merge3Tables
from Task1Methods.MeanValue import CompleteByMean
from Task1Methods.KNN import CompleteByKNN


# set the max row and column numbers for printing
pd.set_option('display.max_rows',1000)
pd.set_option('display.max_columns',1000)


# Open the xlsx file by using 'openpyxl' and save 3 sheets
file_path = 'China Lake.xlsx'
sheets = pd.read_excel(file_path, engine='openpyxl', sheet_name=[0, 1, 2])
CHLA = sheets[0]
TEMPERATURE = sheets[1]
TOTALP = sheets[2]

# clean sheets: 1. drop irrelevant date, year, depth and station
#               2. merge three tables
#               3. calculate mean value for each month from May to October
#               4. insert 'NaN' to missing month
df = merge3Tables(CHLA, TEMPERATURE, TOTALP)
# save a table for each variable, each table has a 'Date', 'Depth' and the variable column
cleaned_CHLA = pd.DataFrame({'Date': df['Date'], 'Depth': 7, df.columns.values[6]: df.iloc[:, 6]})
cleaned_TEMPERATURE = pd.DataFrame({'Date': df['Date'], 'Depth': 7, df.columns.values[7]: df.iloc[:, 7]})
cleaned_TOTALP = pd.DataFrame({'Date': df['Date'], 'Depth': 7, df.columns.values[8]: df.iloc[:, 8]})

# complete missing data by using 'Mean Value'
complete_CHLA_Mean = CompleteByMean(cleaned_CHLA)
complete_TEMPERATURE_Mean= CompleteByMean(cleaned_TEMPERATURE)
complete_TOTALP_Mean = CompleteByMean(cleaned_TOTALP)

# complete missing data by using 'KNN'
complete_CHLA_KNN = CompleteByKNN(cleaned_CHLA)
complete_TEMPERATURE_KNN = CompleteByKNN(cleaned_TEMPERATURE)
complete_TOTALP_KNN = CompleteByKNN(cleaned_TOTALP)

# concat three sheets to one sheet
df_cleaned = pd.DataFrame({"MIDAS":5448, "Lake":"China Lake", "Town":"China, Vassalboro", "Station":1,
                       "Date":complete_CHLA_KNN['Date'], "Depth":7, "CHLA (mg/L)":cleaned_CHLA.iloc[:, 2],
                  "TEMPERATURE (Centrigrade)":cleaned_TEMPERATURE.iloc[:, 2],
                   "Total P (mg/L)":cleaned_TOTALP.iloc[:, 2]})

df_Mean = pd.DataFrame({"MIDAS":5448, "Lake":"China Lake", "Town":"China, Vassalboro", "Station":1,
                       "Date":complete_CHLA_Mean['Date'], "Depth":7, "CHLA (mg/L)":complete_CHLA_Mean.iloc[:, 6],
                  "TEMPERATURE (Centrigrade)":complete_TEMPERATURE_Mean.iloc[:, 6],
                   "Total P (mg/L)":complete_TOTALP_Mean.iloc[:, 6]})

df_KNN = pd.DataFrame({"MIDAS":5448, "Lake":"China Lake", "Town":"China, Vassalboro", "Station":1,
                       "Date":complete_CHLA_KNN['Date'], "Depth":7, "CHLA (mg/L)":complete_CHLA_KNN.iloc[:, 6],
                  "TEMPERATURE (Centrigrade)":complete_TEMPERATURE_KNN.iloc[:, 6],
                   "Total P (mg/L)":complete_TOTALP_KNN.iloc[:, 6]})

# save excel files to local
df_cleaned.to_excel("China Lake_cleaned.xlsx", index=False)
df_Mean.to_excel("China Lake_Mean.xlsx", index=False)
df_KNN.to_excel("China Lake_KNN.xlsx", index=False)
