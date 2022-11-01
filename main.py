# Loading logging configuration
import configurations
import logging
logger = logging.getLogger("WorkflowExecutor")
logger.info("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
logger.info("Starting...")


import datetime

from broker import Broker
from algo import Algorithm
from position_management import PositionsManager

from alice_blue import AliceBlue
from alice_blue import LiveFeedType, HistoricalDataType

from models import Script
from utils import round_off
import csv
import time
from dateutil import relativedelta

from constants import *

from aliceblue_v2 import Alice



algo = Algorithm()


def callback(script):
    print(script)
    algo.process(script)


class WorkflowExecutor:

    def __init__(self):
        self.broker = Broker()
        self.position_manager = PositionsManager()
        self.nfo_data, self.eq_set, self.expiry_date = None, None, None
        self._initialize_db()

    def execute(self):
        db = Script.get_db()
        fr = datetime.datetime(2022, 10, 28)
        to = datetime.datetime(2022, 10, 29)
        import ipdb; ipdb.set_trace()
        self.broker.subscribe([self.broker.get_instrument_by_symbol("NFO", "AXISBANK22NOV910CE")], callback)
        time.sleep(10)
        # x = self.broker.client.historical_data(self.broker.client.get_instrument_by_symbol("NFO", "AXISBANK22NOV910CE"), fr, to, HistoricalDataType.Minute)
        # print(x)
        for instrument in self.nfo_data:
            script = Script.get_script(instrument.symbol)
            eq_script = Script.get_script(script.eq_symbol)

            # print(entity)
            pc = script.ltp
            ltp = script.ltp
            pcd = round_off(pc*(1 + 0.095))
            trigger_range = self._range_tolerance(pcd)
            sl = round_off(pcd * (1 - 0.05))
            tgt1 = round_off(pcd * (1 + 0.16))
            tgt2 = round_off(pcd * (1 + 0.24))
            tgt3 = round_off(pcd * (1 + 0.35))

            if ltp < 5.00:
                print("Ignoring script: {} as price {} is below 5".format(script.symbol, ltp))
                continue

            print("=============REGULAR BUY=============")
            print("NAME: {}".format(script.symbol))
            print("EQ CLOSE: {}".format(eq_script.ltp))
            print("EQ DERIVED CLOSE: {}".format(self.get_rounded_close(eq_script.close)[0 if script.option_type == OptionType.CE else 1]))
            print("STRIKE: {}".format(script.strike_price))
            print("Expiry: {}".format(script.expiry))
            print("Close: {}".format(script.ltp))
            print("LOT SIZE: {}".format(script.lot_size))
            print("ENTRY RANGE WITH TOLERANCE 0.5%: {}".format(trigger_range))
            print("SL: {}".format(sl))
            print("TARGET 1: {}".format(tgt1))
            print("TARGET 2: {}".format(tgt2))
            print("TARGET 3: {}".format(tgt3))
            print("CAPITAL REQUIRED FOR 1 LOT: {}".format(float(script.lot_size) * pcd))
            print("=====================================")

    def _initialize_db(self):
        self.nfo_data, self.eq_set, self.expiry_date = self.broker.get_nfo_data(self._get_date())
        updated_nfo_data = []
        for instrument in self.eq_set:
            eq_instrument = self.broker.get_instrument_by_symbol("NSE", instrument.eq)
            eq_script = self.broker.get_script_info(eq_instrument)
            ce_instrument, ce_close, pe_instrument, pe_close = self._find_instruments(eq_script.symbol, eq_script.close)
            ce_script, pe_script = self.broker.get_script_info(ce_instrument), self.broker.get_script_info(pe_instrument)
            ce_script.derived_from, pe_script.derived_from = ce_close, pe_close
            self.position_manager.update_script(eq_script)
            self.position_manager.update_script(ce_script)
            self.position_manager.update_script(pe_script)
            updated_nfo_data.append(ce_instrument)
            updated_nfo_data.append(pe_instrument)
        print("Scripts: " + str(len(Script.get_db()) // 3))
        self.nfo_data = updated_nfo_data

    def _find_instruments(self, eq, close) -> tuple:
        ce_close, pe_close = self.get_rounded_close(close)
        return min(filter(lambda x: x.option_type == OptionType.CE.value and x.eq == eq, self.nfo_data),
                   key=lambda x: abs(x.strike_price - ce_close)), ce_close, \
               min(filter(lambda x: x.option_type == OptionType.PE.value and x.eq == eq, self.nfo_data),
                   key=lambda x: abs(x.strike_price - pe_close)), pe_close

    def get_rounded_close(self, value):
        return float(value) * (1 + 0.0075), float(value) * (1 - 0.0075)

    def _range_tolerance(self, value):
        # value = round_off(value, 2)
        return [round_off(value * (1 - 0.005), 2), value, round_off(value * (1 + 0.005), 2)]

    def _get_date(self):
        # date = input("Enter Date: ")
        # try:
        #     now = datetime.datetime.strptime(date, '%d-%m-%Y')
        # except:
        #     now = datetime.datetime.now()
        # return now
        return datetime.datetime.now()


def main():
    # pass
    we = WorkflowExecutor()
    we.execute()
    import ipdb; ipdb.set_trace()
    logger.info("Exited...")
    logger.info("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")


if __name__ == '__main__':
    main()
