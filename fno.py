import datetime
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen

GENERIC_URL = "https://archives.nseindia.com/content/historical/DERIVATIVES/{}/{}/fo{}bhav.csv.zip"
FILE_NAME = "fo{}"


class FnOData:

    def __init__(self):
        # Download csv or check if already exist & set dict into self.csv_data
        self.csv_data = []
        self.next_expiry_date = datetime.datetime.now()
        x = datetime.datetime.now()
        now = datetime.datetime.now()
        # Change x to correct datetime based on time
        file = FILE_NAME.format(x.strftime("%d%b%Y").upper())
        url = GENERIC_URL.format(x.year, x.strftime("%b").upper(), x.strftime("%d%b%Y").upper())
        # check if file exist if not fetch with url
        pass

    def get_closest_ce_pe_with_strike_price(self, symbol, ce_eq_close, pe_eq_close):
        # input - "AXISBANK", 807.00, 794.90
        # Extract values from self.csv_data
        # Decide which expiry to pick
        # return expiry_date, ce_strike, ce_close, pe_strike, pe_close
        return "2022-10-27", 800.00, 5.60, 800.00, 69.95

    def get_fno_list(self):
        return ["AXISBANK"]

# resp = urlopen(url)
# myzip = ZipFile(BytesIO(resp.read()))
# csv = []
# for line in myzip.open(file).readlines():
#     csv.append(line.decode('utf-8'))
#
# class csv_data:
#
#     def __init__(self,dtype,symbol,date):
#         self.dtype = dtype
#         self.symbol = symbol
#         self.date = date
#         self.value = value
#
#
#     def get_data(self):
#         return self.dtype,self.symbol,self.date
#
#
#
# x = list(filter(lambda y: y.split(',')[4] == raj.dtype and y.split(',')
#          [1] == raj.symbol and y.split(',')[2] == raj.date, csv))
#
# def closest_value(, input_value):
#     def difference(input_list):
#      return abs(input_list - input_value)
#     res = min(input_list, key=difference)
#     return res
#
# closest_value(map(lambda y: float(y.split(',')[3]), x), 19030)





