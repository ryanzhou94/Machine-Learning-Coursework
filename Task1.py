import pandas as pd
import numpy as np
from utility import clean
from MeanValue import CompleteByMean

pd.set_option('display.max_rows',1000)


# Open 'China Lake.xlsx' and read 3 sheets
file_path = 'China Lake.xlsx'

# Open the xlsx file by using 'openpyxl'
sheets = pd.read_excel(file_path, engine='openpyxl', sheet_name=[0, 1, 2])

# Save 3 sheets
CHLA = sheets[0]        # target_name = 'CHLA （mg/L）'
TEMPERATURE = sheets[1] # target_name = 'TEMPERATURE（Centrigrade）'
TOTALP = sheets[2]      # target_name = 'Total P （mg/L）'


cleaned_sheet = clean(sheet=CHLA)
df = CompleteByMean(cleaned_sheet)

