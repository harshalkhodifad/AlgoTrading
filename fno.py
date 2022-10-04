from urllib.request import urlopen
from zipfile import ZipFile
from io import BytesIO

url = "https://archives.nseindia.com/content/historical/DERIVATIVES/2022/SEP/fo30SEP2022bhav.csv.zip"
file = "fo30SEP2022bhav.csv"

resp = urlopen(url) 
myzip = ZipFile(BytesIO(resp.read()))

for line in myzip.open(file).readlines():
     print(line.decode('utf-8'))

