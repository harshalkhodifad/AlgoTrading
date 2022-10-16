import datetime
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
import os

GENERIC_URL = "https://archives.nseindia.com/content/historical/DERIVATIVES/{}/{}/fo{}bhav.csv.zip"
FILE_NAME = "fo{}"

class FnOData:

    def __init__(self):
        # Download csv or check if already exist & set dict into self.csv_data
        self.csv_data = self._download_fno_data_from_nse()
        self.next_expiry_date = self._get_expiry_date()
        # Change x to correct datetime based on time

        
    def get_closest_ce_pe_with_strike_price(self, symbol, ce_eq_close, pe_eq_close):
        # input - "AXISBANK", 807.00, 794.90
        x = list(filter(lambda y: y.split(',')[4] == "CE" and y.split(',')
        [1] == symbol, self.csv_data))
        def closest_value(input_list ,input_value):
            def difference(input_list):
                return abs(input_list - input_value)
            res = min(input_list, key=difference)
            return res

        ce_strike = closest_value(map(lambda y: float(y.split(',')[3]), x), ce_eq_close)
        for i,j in enumerate(x):
            if float(x[i].split(',')[3]) == ce_strike and datetime.datetime.now().strftime('%b') in x[i].split(',')[2]:
                ce_close = x[i].split(',')[8]

        print(ce_strike,ce_close)
        # Decide which expiry to pick
        # return expiry_date, ce_strike, ce_close, pe_strike, pe_close
        return "2022-10-27", 800.00, 5.60, 800.00, 69.95

    def get_fno_list(self):
        return ["AXISBANK"]

    def _download_fno_data_from_nse(self):
        # TODO: Use header mapping while accessing by index - as csv header can change
        now = datetime.datetime.now()
        x = now - datetime.timedelta(days=3)
        file = FILE_NAME.format(x.strftime("%d%b%Y").upper())
        local_file_path = "resources/{}bhav.csv".format(file, file)
        url = GENERIC_URL.format(x.year, x.strftime("%b").upper(), x.strftime("%d%b%Y").upper())
        if os.path.isfile(local_file_path):
        # check if file exist if not fetch with url
            resp = urlopen(url)
            myzip = ZipFile(BytesIO(resp.read()))
            myzip.extractall('resources/')
        csv_data = []
        for i, line in enumerate(open(local_file_path).readlines()):
            if i==0:
                continue
            csv_data.append(line)
        return csv_data

    def _get_expiry_date(self):
        pass

def main():
    import ipdb; ipdb.set_trace()
    fno = FnOData()
    fno.get_closest_ce_pe_with_strike_price("AXISBANK", 807.00, 794.90)
    

if __name__ == "__main__":
    main()

# csv = []

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
#

#






