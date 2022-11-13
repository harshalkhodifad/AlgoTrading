import configurations
import statistics
import logging

import datetime
import os.path
import pickle
from typing import Dict

from broker import AliceClient, Broker
from alice_blue import HistoricalDataType, Instrument
from models import *
from utils import *

# print("Started: {}".format(datetime.datetime.now()))

scripts = {

}

# fetch list -> if not available ignore
# one by one script
# multiple targets

logger = logging.getLogger("BACKTEST")
year = int(input("Enter year: "))
st = datetime.datetime(year, 1, 1)
et = datetime.datetime(year+1, 1, 1)
file_name = st.strftime("resources/eq_nifty_50_data_%Y.pickle")
csv_name = st.strftime("resources/eq_nifty_50_data_%Y.csv")
hst = []
if os.path.isfile(file_name):
    # logger.info("Reading from file")
    hst = read_file(file_name)
else:
    # logger.info("Fetching data")
    broker = Broker()
    inst = broker.get_instrument_by_symbol("NSE", "AXISBANK-EQ")
    import ipdb; ipdb.set_trace()
    while True:
        print("Fetching for: ")
        print(st)
        mt = datetime.timedelta(days=2) + st
        ett = min(mt, et)
        data = broker.get_historical_data(inst, st, ett)
        hst.extend(data)
        if mt >= et:
            break
        st = mt

write_file(hst, file_name)
import ipdb; ipdb.set_trace()
write_csv(hst, csv_name)


def main():
    pass


if __name__ == "__main__":
    main()

