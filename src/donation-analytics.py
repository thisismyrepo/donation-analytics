# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 22:16:26 2018

@author: Thinkpad
"""

import math
import re
import pandas as pd
import numpy as np



input_file = "/input/itcont.txt"
fileHandle = open('input_file', 'r')       # Opening input file "itcont.txt"

#fileHandle = """
#+C00629618|N|TER|P|201701230300133512|15C|IND|PEREZ, JOHN A|LOS ANGELES|CA|90017|PRINCIPAL|DOUBLE NICKEL ADVISORS|01032017|40|H6CA34245|SA01251735122|1141239|||2012520171368850783
#+C00177436|N|M2|P|201702039042410894|15|IND|DEEHAN, WILLIAM N|ALPHARETTA|GA|300047357|UNUM|SVP, SALES, CL|01312017|384||PR2283873845050|1147350||P/R DEDUCTION ($192.00 BI-WEEKLY)|4020820171370029337
#+C00384818|N|M2|P|201702039042412112|15|IND|ABBOTT, JOSEPH|WOONSOCKET|RI|028956146|CVS HEALTH|VP, RETAIL PHARMACY OPS|01122017|250||2017020211435-887|1147467|||4020820171370030285
#+C00384516|N|M2|P|201702039042410893|15|IND|SABOURIN, JAMES|LOOKOUT MOUNTAIN|GA|028956146|UNUM|SVP, CORPORATE COMMUNICATIONS|01312017|230||PR1890575345050|1147350||P/R DEDUCTION ($115.00 BI-WEEKLY)|4020820171370029335
#+C00177436|N|M2|P|201702039042410895|15|IND|JEROME, CHRISTOPHER|LOOKOUT MOUNTAIN|GA|307502818|UNUM|EVP, GLOBAL SERVICES|10312017|384||PR2283905245050|1147350||P/R DEDUCTION ($192.00 BI-WEEKLY)|4020820171370029342
#+C00384516|N|M2|P|201702039042412112|15|IND|ABBOTT, JOSEPH|WOONSOCKET|RI|028956146|CVS HEALTH|EVP, HEAD OF RETAIL OPERATIONS|01122018|333||2017020211435-910|1147467|||4020820171370030287
#+C00384516|N|M2|P|201702039042410894|15|IND|SABOURIN, JAMES|LOOKOUT MOUNTAIN|GA|028956146|UNUM|SVP, CORPORATE COMMUNICATIONS|01312018|384||PR2283904845050|1147350||P/R DEDUCTION ($192.00 BI-WEEKLY)|4020820171370029339
#"""
for line in fileHandle:
    fields = line.split('|')
    
# get percentile value from percentile.txt
input_file2 = "/input/percentile.txt"
PercentileToCalculate= open('input_file2', 'r')   
# PercentileToCalculate = 30


input_data = re.sub(r'(C0)', r'|\1', fileHandle)   
fields = input_data.split('|')                       # Splits data into separate indices
del fields[0]
counter = 0


NumberOfRows = round(len(fields)/21)
NumberOfCols = 6


df = pd.DataFrame(fields)
data = pd.DataFrame(df.values.reshape(-1,21), index = range(NumberOfRows), columns = ['CMTE_ID', 2, 3, 4, 5, 6, 7, 'NAME', 9, 10, 'ZIP_CODE', 12, 13, 'TRANSACTION_DT', 'TRANSACTION_AMT', 'OTHER_ID', 17, 18, 19, 20, 21])
newdata = data    # make a copy of the data frame
#for i in range(NumberOfRows):

# Detect repeat donors. 

outputfile = open('/output/repeat_donors.txt','w') 

i = 1
while i <= NumberOfRows:   # compare values in CMTE_ID column to see if any are the same. If so, output that ID and other info.
    for j in range((i-1),-1,-1):                                             # for(j=i; j>=0; j=j-1)
        if newdata.iloc[i]['CMTE_ID'] == newdata.iloc[j]['CMTE_ID']:
            CMTE_ID = newdata.iloc[i]['CMTE_ID']
            ZIP_CODE = newdata.iloc[i]['ZIP_CODE'][:5]             # get first 5 digits of zipcode
            TRANSACTION_YEAR = newdata.iloc[i]['TRANSACTION_DT'][-4:]   
            
            mask = newdata['CMTE_ID'] == CMTE_ID                   # select all rows that have the same ID
            newdata2 = newdata[mask]                               # make a new dataframe with only those rows
            HowManyTransactions = len(newdata2.index)
            OrdinalRank = math.ceil((PercentileToCalculate/100)*HowManyTransactions)
            TotalAmount = float(newdata.iloc[i]['TRANSACTION_AMT']) + float(newdata.iloc[j]['TRANSACTION_AMT'])
            newdata2.sort_values('TRANSACTION_AMT')
            CalculatedPercentileValue = newdata2.iloc[OrdinalRank]['TRANSACTION_AMT']
            #CalculatedPercentileValue = newdata.TRANSACTION_AMT.quantile(PercentileToCalculate/100)
            #TotalAmount = newdata2['TRANSACTION_AMT'].sum()
            
            
            #print(i,j)
            print(CMTE_ID, '|', ZIP_CODE, '|', TRANSACTION_YEAR, '|', CalculatedPercentileValue, '|', TotalAmount, '|', HowManyTransactions)
            break
            outputfile.write(CMTE_ID, '|', ZIP_CODE, '|', TRANSACTION_YEAR, '|', CalculatedPercentileValue, '|', TotalAmount, '|', HowManyTransactions)
    i = i+1
    newdata = data
# For each repeat donor, calculate percentile, total amount of contributions, and total number of transactions.

# Output: CMTE_ID|ZIP_CODE|YEAR|PERCENTILE_VALUE|TotalAmount|HowManyTransactions

#•	recipient of the contribution (or CMTE_ID from the input file)
#•	5-digit zip code of the contributor (or the first five characters of the ZIP_CODE field from the input file)
#•	4-digit year of the contribution
#•	running percentile of contributions received from repeat donors to a recipient streamed in so far for this zip code and calendar year. Percentile calculations should be rounded to the whole dollar (drop anything below $.50 and round anything from $.50 and up to the next dollar)
#•	total amount of contributions received by recipient from the contributor's zip code streamed in so far in this calendar year from repeat donors
#•	total number of transactions received by recipient from the contributor's zip code streamed in so far this calendar year from repeat donors

 

    