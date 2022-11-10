# AlgoTrading

## Setup Instructions:
```commandline
git clone git@github.com:harshalkhodifad/AlgoTrading.git
cd AlgoTrading
sudo apt-get install python3-venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Logic

1. Fetch F&O list
2. Interaction with live data
3. Order placement interaction => (Dummy + Actual)
4. Output order history - unique order id + event type (Print) => Every 5 seconds print whole trades open/closed + Generate PnL by every order
5. Algo logic - strategy -> 



1. Fetch F&O
   - get_fno_list() -> ['A', 'B']
   - get_equity_data('A', 540.6*(1.0075), 540*(1-0.0075))=> round() => 2022-10-27, Closest CE strike price, CE's close, Closest PE Strike price, PE's close

  NFO,ADANIPORTS,60563,OPTSTK,2022-10-27,CE,780.0,1250.0,ADANIPORTS22OCT780CE
  NFO,ADANIPORTS,60564,OPTSTK,2022-10-27,PE,780.0,1250.0,ADANIPORTS22OCT780PE

from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
# or: requests.get(url).content

url = "https://archives.nseindia.com/content/historical/DERIVATIVES/2022/SEP/fo30SEP2022bhav.csv.zip"
file = "fo30SEP2022bhav.csv"

resp = urlopen(url)
myzip = ZipFile(BytesIO(resp.read()))
csv = []
for line in myzip.open(file).readlines():
    csv.append(line.decode('utf-8'))

x = list(filter(lambda y: y.split(',')[4]=='CE' and y.split(',')[1]=='NIFTY' and y.split(',')[2]=='01-Dec-2022', csv))
closest_value(map(lambda y: float(y.split(',')[3]), x), 19030)

def closest_value(input_list, input_value):
  difference = lambda input_list : abs(input_list - input_value)
  res = min(input_list, key=difference)
  return res
2. 






--------------------------------------------


Aarti industries: 745.20
 +0.75%  => 750.789 => round(0.05) => 750.80 
 => 750 Strike price for CE => Previous Close price: 28.05 => *(1.095) => 30.71475 => 30.70 => (30.55(Entry trigger) - 30.7, 30.7 - 30.85(Entry trigger)) => (30.6, 30.8) => SL: 29.15(5%) + 0.5% => 29.30 (SL Trigger)

TARGET 1 - 16% TARGET 2 - 24% AND TARGET 3 - 35% FROM ENTRY PRICE - FOR ALL Entry types.
 
 -- REGULAR ENTRY only if option price stays above previous close.
 
 Example: [Targets: , T1: 35.60, T2: ]
 1. E: 30.7, Max SL: 29.15 => 
 Set trailing SL only after T1.
 
 30.7 -> 35.6 + 1% = 35.95 => 35.6 SL
 
 Set target 2 + 1% tolerance when price is target 1 + 5%.
 
 Don't set target or sl in broker.
 
 Set SL when (30.7 - 29.15) = 1.55*0.4 = 0.62 => 0.6 => (30.7-0.6) => 30.1 => Put SL order.
 
 
 
 -- REVISED 1:
 Option price stays above -18% from previous close - 28.05 => 23.
 Entry price: +10% current day low (i.e. 24 current day low => 26.4 + tolerance => SL(5%) => Targets as mentioned above)
 
  -- REVISED 2:
   Option price breaks -18% from previous close - 28.05 => 23.
 Entry price: +12% current day low (i.e. 20 current day low => 22.4 + tolerance => SL(5%) => Targets as mentioned above)


Trailing stoploss: [After crossing target 3]
 
 Tolerance: 0.5%
 
 - Fetch data one day earlier rather than in morning.