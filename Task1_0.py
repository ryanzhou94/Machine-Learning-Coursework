import pandas as pd
from utility import clean
from Task1Methods.MeanValue import CompleteByMean
from Task1Methods.KNN import CompleteByKNN

# set the max row and column numbers for printing
pd.set_option('display.max_rows',1000)
pd.set_option('display.max_columns',1000)


# Open the xlsx file by using 'openpyxl' and save 3 sheets
file_path = 'China Lake.xlsx'
sheets = pd.read_excel(file_path, engine='openpyxl', sheet_name=[0, 1, 2])
CHLA = sheets[0]        # target_name = 'CHLA （mg/L）'
TEMPERATURE = sheets[1] # target_name = 'TEMPERATURE（Centrigrade）'
TOTALP = sheets[2]      # target_name = 'Total P （mg/L）'


# clean sheets: 1. drop irrelevant date, year and depth
#               2. calculate the mean value for each month from May to October
#               3. add 'NaN' to missing month
cleaned_CHLA = clean(df=CHLA)
cleaned_TEMPERATURE = clean(df=TEMPERATURE)
cleaned_TOTALP = clean(df=TOTALP)


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
                       "Date":complete_CHLA_KNN['Date'].dt.date, "Depth":7, "CHLA (mg/L)":cleaned_CHLA.iloc[:, 2],
                  "TEMPERATURE (Centrigrade)":cleaned_TEMPERATURE.iloc[:, 2],
                   "Total P (mg/L)":cleaned_TOTALP.iloc[:, 2]})

df_Mean = pd.DataFrame({"MIDAS":5448, "Lake":"China Lake", "Town":"China, Vassalboro", "Station":1,
                       "Date":complete_CHLA_Mean['Date'].dt.date, "Depth":7, "CHLA (mg/L)":complete_CHLA_Mean.iloc[:, 6],
                  "TEMPERATURE (Centrigrade)":complete_TEMPERATURE_Mean.iloc[:, 6],
                   "Total P (mg/L)":complete_TOTALP_Mean.iloc[:, 6]})

df_KNN = pd.DataFrame({"MIDAS":5448, "Lake":"China Lake", "Town":"China, Vassalboro", "Station":1,
                       "Date":complete_CHLA_KNN['Date'].dt.date, "Depth":7, "CHLA (mg/L)":complete_CHLA_KNN.iloc[:, 6],
                  "TEMPERATURE (Centrigrade)":complete_TEMPERATURE_KNN.iloc[:, 6],
                   "Total P (mg/L)":complete_TOTALP_KNN.iloc[:, 6]})


# save excel files to local
df_cleaned.to_excel("China Lake_cleaned.xlsx", index=False)
df_Mean.to_excel("China Lake_Mean.xlsx", index=False)
df_KNN.to_excel("China Lake_KNN.xlsx", index=False)
