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
eq_list = get_nifty_500_list()
broker = Broker()
for i, eq in enumerate(eq_list):
    inst = broker.get_instrument_by_symbol("NSE", eq+"-EQ")
    st = datetime.datetime(2021, 1, 1)
    et = datetime.datetime(2022, 1, 1)
    hst = []
    csv_name = st.strftime(f"resources/eq_data/{inst.symbol}_data_%Y.csv")
    while True:
        logger.info(f"Fetching for: {i+1}th equity: {eq}, for 2 days from: {st}")
        mt = datetime.timedelta(days=2) + st
        ett = min(mt, et)
        data = broker.get_historical_data(inst, st, ett)
        hst.extend(data)
        if mt >= et:
            break
        st = mt
    write_csv(hst, csv_name)


def main():
    pass


if __name__ == "__main__":
    main()

