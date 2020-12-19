import pandas as pd
import numpy as np
import time

# pseudo-code:
#   1. Read the excel file: 'China Lake'
#   2. Save 3 sheets
#       a. 可以考虑把前面的三条数据删除，因为三张表，每条数据都一样，以此提升性能
#   3. Select one depth (3 sheets use 1 depth: 7) and drop other data
#       a. Depth: 7
#   4. Select valid month (May - October)
#       a. Date数据第一个/前的数字:5~10
#   5. Calculate mean value of each month
#   6. Find missing months
#       a. 10后面不是5，5后面不是6，6后面不是7，...，9后面不是10
#       b. 插入一条新的数据，月份自动计算
#       c. 使用Mean Value来计算目标数据
#           1). 中间数据缺失：用前一个月和后一个月的平均值
#           2). 头（五月）或者尾（十月）数据缺失：用两倍的相邻月减去第二相邻月
#           3). 连续缺失：用前两个或后两个月来计算缺失的第一个月，再用补足的月份来计算剩下的

# Open 'China Lake.xlsx' and read 3 sheets
file_path = 'China Lake.xlsx'
# Open the xlsx file by using 'openpyxl'
sheets = pd.read_excel(file_path, engine='openpyxl', sheet_name=[0, 1, 2])
# Save 3 sheets
CHLA = sheets[0]
TEMPERATURE = sheets[1]
TOTALP = sheets[2]

print([column for column in CHLA])
# ['MIDAS', 'Lake', 'Town', 'Station', 'Date', 'Depth', 'CHLA （mg/L）']
# ['MIDAS', 'LAKE', 'Town(s)', 'STATION', 'Date', 'DEPTH', 'TEMPERATURE（Centrigrade）']
# ['MIDAS', 'Lake', 'Town(s)', 'Station', 'Date', 'Depth', 'Total P （mg/L）']

## Processs 'CHLA':
# We will only process the date, depth, target item (CHLA, TEMPERATUR and Total P),
# therefor, we drop irrelevant items, which are MIDAS, LAKE, Town(s) and STATION
# With the reduced amount of data, the program will process data much faster
df = CHLA.loc[:, ['Date', 'Depth', 'CHLA （mg/L）']]
# print(df)
#           Date  Depth  CHLA （mg/L）
# 0   1988-05-04   10.0       0.0117
# 1   1988-05-26   10.0       0.0041
# 2   1988-06-10   10.0       0.0042
# 3   1988-06-29    8.0       0.0052
# 4   1988-07-13    6.0       0.0058
# ..         ...    ...          ...
# 609 2013-08-15    7.0       0.0150


# Select an appropriate depth(7) by dropping irrelevant depths
df.drop(df[df.Depth != 7].index, inplace=True)
df.reset_index(drop=True, inplace=True)

# Select an appropriate time period by dropping irrelevant years
# Analyzing three sheets, 1998-2013 is an appropriate time period
start = pd.to_datetime('1998-5-1')
end = pd.to_datetime('2013-11-1')
df.drop(df[df.Date < start].index, inplace=True)
df.drop(df[df.Date >= end].index, inplace=True)
df.reset_index(drop=True, inplace=True)

print(df)





