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
from dummy_data import feed_dummy_data

from alice_blue import AliceBlue
from alice_blue import LiveFeedType, HistoricalDataType

from models import Script
from utils import round_off
import csv
import time
from dateutil import relativedelta

from constants import *

from aliceblue_v2 import Alice


broker = Broker()
position_manager = PositionsManager()
algo = Algorithm(position_manager)
square_off_in_progress = False


def callback(script):
    global square_off_in_progress
    algo.process(script, square_off_in_progress)


class WorkflowExecutor:

    def __init__(self, brker: Broker, positionManager: PositionsManager):
        self.broker = brker
        self.position_manager = positionManager
        self.nfo_data, self.eq_set, self.expiry_date = None, None, None
        self._initialize_db()

    def start(self):
        while not self.should_execute():
            time.sleep(1)
        self.execute()

    def execute(self):
        print("Starting trade executions")
        # import ipdb; ipdb.set_trace()
        # self.broker.subscribe([self.broker.get_instrument_by_symbol("NFO", "AXISBANK22NOV880CE")], callback)
        self.broker.subscribe(self.nfo_data, callback)
        # feed_dummy_data(callback)

        while True:
            time.sleep(1)
            print("Running")
            if self.exit_if_required():
                break

        # fr = datetime.datetime(2022, 10, 28)
        # to = datetime.datetime(2022, 10, 29)
        # x = self.broker.client.historical_data(self.broker.client.get_instrument_by_symbol("NFO", "AXISBANK22NOV910CE"), fr, to, HistoricalDataType.Minute)
        # print(x)

    def should_execute(self):
        now = datetime.datetime.now()
        if (now.hour * 60 + now.minute) >= (9*60 + 20):
            return True
        else:
            return False

    def exit_if_required(self):
        global square_off_in_progress
        now = datetime.datetime.now()
        if now.hour == 15 and now.minute == 15:
            square_off_in_progress = True
            self.broker.unsubscribe(self.nfo_data)
            print("Square off initiated")
            logger.info("Square off initiated")
            algo.square_off()
            print("Square off completed")
            logger.info("Square off completed")
            return True
        else:
            return False

    def _initialize_db(self):
        logger.info("Fetching F&O Data")
        self.nfo_data, self.eq_set, self.expiry_date = self.broker.get_nfo_data(self._get_date())
        updated_nfo_data = []
        i = 0
        for instrument in self.eq_set:
            print(i)
            i+=1
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
        self.position_manager.init_position_locks()
        # TO CHANGE - Remove banned script
        logger.info("Fetched F&O Data, Total Instruments: " + str(len(Script.get_db()) // 3))
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
    logger.info("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    we = WorkflowExecutor(broker, position_manager)
    we.start()
    logger.info("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")


if __name__ == '__main__':
    main()
