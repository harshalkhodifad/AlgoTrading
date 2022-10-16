from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen

url = "https://archives.nseindia.com/content/historical/DERIVATIVES/2022/SEP/fo30SEP2022bhav.csv.zip"
file = "fo30SEP2022bhav.csv"

resp = urlopen(url)
myzip = ZipFile(BytesIO(resp.read()))
csv = []
for line in myzip.open(file).readlines():
    csv.append(line.decode('utf-8'))

class csv_data:

    def __init__(self,dtype,symbol,date):
        self.dtype = dtype
        self.symbol = symbol
        self.date = date
        self.value = value


    def get_data(self):
        return self.dtype,self.symbol,self.date



x = list(filter(lambda y: y.split(',')[4] == raj.dtype and y.split(',')
         [1] == raj.symbol and y.split(',')[2] == raj.date, csv))

def closest_value(, input_value):
    def difference(input_list): 
     return abs(input_list - input_value)
    res = min(input_list, key=difference)
    return res

closest_value(map(lambda y: float(y.split(',')[3]), x), 19030)





