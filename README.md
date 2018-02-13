This code uses the following libraries:
import math
import re
import pandas as pd
import numpy as np

2 input files needed: itcont.txt, percentile.txt

Sample itcont.txt:
+C00629618|N|TER|P|201701230300133512|15C|IND|PEREZ, JOHN A|LOS ANGELES|CA|90017|PRINCIPAL|DOUBLE NICKEL ADVISORS|01032017|40|H6CA34245|SA01251735122|1141239|||2012520171368850783
+C00177436|N|M2|P|201702039042410894|15|IND|DEEHAN, WILLIAM N|ALPHARETTA|GA|300047357|UNUM|SVP, SALES, CL|01312017|384||PR2283873845050|1147350||P/R DEDUCTION ($192.00 BI-WEEKLY)|4020820171370029337
+C00384818|N|M2|P|201702039042412112|15|IND|ABBOTT, JOSEPH|WOONSOCKET|RI|028956146|CVS HEALTH|VP, RETAIL PHARMACY OPS|01122017|250||2017020211435-887|1147467|||4020820171370030285
+C00384516|N|M2|P|201702039042410893|15|IND|SABOURIN, JAMES|LOOKOUT MOUNTAIN|GA|028956146|UNUM|SVP, CORPORATE COMMUNICATIONS|01312017|230||PR1890575345050|1147350||P/R DEDUCTION ($115.00 BI-WEEKLY)|4020820171370029335
+C00177436|N|M2|P|201702039042410895|15|IND|JEROME, CHRISTOPHER|LOOKOUT MOUNTAIN|GA|307502818|UNUM|EVP, GLOBAL SERVICES|10312017|384||PR2283905245050|1147350||P/R DEDUCTION ($192.00 BI-WEEKLY)|4020820171370029342
+C00384516|N|M2|P|201702039042412112|15|IND|ABBOTT, JOSEPH|WOONSOCKET|RI|028956146|CVS HEALTH|EVP, HEAD OF RETAIL OPERATIONS|01122018|333||2017020211435-910|1147467|||4020820171370030287
+C00384516|N|M2|P|201702039042410894|15|IND|SABOURIN, JAMES|LOOKOUT MOUNTAIN|GA|028956146|UNUM|SVP, CORPORATE COMMUNICATIONS|01312018|384||PR2283904845050|1147350||P/R DEDUCTION ($192.00 BI-WEEKLY)|4020820171370029339

Sample percentile.txt:
30

For each recipient, zip code and calendar year, calculate these three values for contributions coming from repeat donors:
•	total dollars received
•	total number of contributions received
•	donation amount in a given percentile

CMTE_ID: identifies the flier, which for our purposes is the recipient of this contribution
NAME: name of the donor
ZIP_CODE: zip code of the contributor (we only want the first five digits/characters)
TRANSACTION_DT: date of the transaction
TRANSACTION_AMT: amount of the transaction
OTHER_ID:  (Skip this value if it’s not empty) a field that denotes whether contribution came from a person or an entity
Other situations you can completely ignore and skip an entire record:
•	If TRANSACTION_DT is an invalid date (e.g., empty, malformed)
•	If ZIP_CODE is an invalid zip code (i.e., empty, fewer than five digits)
•	If the NAME is an invalid name (e.g., empty, malformed)
•	If any lines in the input file contains empty cells in the CMTE_ID or TRANSACTION_AMT fields
Output file
For the output file that your program will create, repeat_donors.txt, the fields on each line should be separated by a |
The output should contain the same number of lines or records as the input data file, itcont.txt, minus any records that were ignored as a result of the 'Input file considerations' and any records you determine did not originate from a repeat donor.
Each line of this file should contain these fields:
•	recipient of the contribution (or CMTE_ID from the input file)
•	5-digit zip code of the contributor (or the first five characters of the ZIP_CODE field from the input file)
•	4-digit year of the contribution
•	running percentile of contributions received from repeat donors to a recipient streamed in so far for this zip code and calendar year. Percentile calculations should be rounded to the whole dollar (drop anything below $.50 and round anything from $.50 and up to the next dollar)
•	total amount of contributions received by recipient from the contributor's zip code streamed in so far in this calendar year from repeat donors
•	total number of transactions received by recipient from the contributor's zip code streamed in so far this calendar year from repeat donors
Example
The seventh record also is for a repeat donor because SABOURIN, JAMES, who contributed Jan. 31, 2018, also contributed Jan. 31, 2017.
When we look for any contributions from repeat donors for recipient, C00384516, zip of 02895 for the year 2018, we would find that the sixth and seventh records qualify. So we would emit
•	the total number of contributions from repeat donors is 2
•	the total dollar amount of contributions is 333 + 384 or 717
•	the 30th percentile contribution is 333
Processing all of the input lines in itcont.txt, the entire contents of repeat_donors.txt would be:
C00384516|02895|2018|333|333|1
C00384516|02895|2018|333|717|2

For the percentile computation use the nearest-rank method as described by Wikipedia.
https://en.wikipedia.org/wiki/Percentile#The_nearest-rank_method
 

