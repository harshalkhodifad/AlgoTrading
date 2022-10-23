import datetime
from alice_blue import AliceBlue
from alice_blue import LiveFeedType

from algo import subscriber_callback, update_script
from models import Script
from utils import round_off
import csv
import time
from dateutil import relativedelta

from constants import *

from aliceblue_v2 import Alice


# alice = Alice(USERNAME, "APP_SECRET")
# alice.session_id = AliceBlue.login_and_get_sessionID(username=USERNAME,
#                                                      password=PASSWORD,
#                                                      twoFA=DOB,
#                                                      app_id=APP_API_KEY,
#                                                      api_secret=APP_SECRET)
# # print(alice.create_session())  # Must "log in" to Alice platform before create session
# alice.download_master_contract(False)  # Download initially once a day
# print(alice.get_profile())
#
# algo = Algo()
# alice.invalidate_socket_session()
# alice.create_socket_session()
# alice.start_websocket(subscribe_callback=Algo.subscription_callback,
#                       socket_open_callback=socket_open_callback,
#                       run_in_background=True)
# while not socket_opened:
#     pass
# print("Websocket : Connected")
# alice.subscribe([alice.get_instrument_by_symbol("NSE", i) for i in ["ACC-EQ", "RELIANCE-EQ", "UPL-EQ", "LUPIN-EQ"]])
# time.sleep(3000)
# alice.unsubscribe([alice.get_instrument_by_symbol("NSE", i) for i in ["ACC-EQ", "RELIANCE-EQ"]])
# time.sleep(10)


class WorkflowExecutor:

    def __init__(self):
        self.alice = self._alice_login()
        self.nfo_data, self.eq_set, self.expiry_date = self.fetch_nfo_data()
        self._initialize_db()

    def _alice_login(self):
        session_id = AliceBlue.login_and_get_sessionID(username=USERNAME,
                                                       password=PASSWORD,
                                                       twoFA=DOB,
                                                       app_id=APP_SECRET,
                                                       api_secret=APP_API_KEY)
        return AliceBlue(username=USERNAME, session_id=session_id)

    def execute(self):
        db = Script.get_db()
        self.alice.start_websocket(subscriber_callback)
        self.alice.subscribe(self.nfo_data, LiveFeedType.TICK_DATA)
        time.sleep(20)
        # self.alice.subscribe([self.alice.get_instrument_by_symbol("NSE", "AXISBANK-EQ")], LiveFeedType.TICK_DATA)
        # SILVERM22NOVFUT
        # self.alice.unsubscribe([self.alice.get_instrument_by_symbol("NSE", "AXISBANK22OCT810CE")], LiveFeedType.TICK_DATA)
        # self.alice.close_websocket()

    #     self.alice.invalidate_socket_session()
    #     self.alice.create_socket_session()
    #     self.alice.start_websocket(subscribe_callback=event_handler_quote_update,
    #                                socket_open_callback=open_callback,
    #                                run_in_background=True)
    #     while not socket_opened:
    #         pass
    #     print("Websocket : Connected")
    #     self.alice.subscribe(
    #         [self.alice.get_instrument_by_symbol("NFO", i) for i in ["AXISBANK22OCT810CE", "AXISBANK22OCT810PE"]])
    #     time.sleep(600)
        for instrument in self.nfo_data:
            script = Script.get_script(instrument.symbol)
            eq_script = Script.get_script(script.eq_symbol)

            # print(entity)
            pc = script.close
            ltp = script.ltp
            pcd = round_off(pc*(1 + 0.095))
            trigger_range = self.range_tolerance(pcd)
            sl = round_off(pcd * (1 - 0.05))
            tgt1 = round_off(pcd * (1 + 0.16))
            tgt2 = round_off(pcd * (1 + 0.24))
            tgt3 = round_off(pcd * (1 + 0.35))

            if ltp < 5.00:
                print("Ignoring script: {} as price {} is below 5".format(script.symbol, ltp))
                continue

            print("=============REGULAR BUY=============")
            print("NAME: {}".format(script.symbol))
            print("EQ CLOSE: {}".format(eq_script.close))
            print("EQ DERIVED CLOSE: {}".format(self.get_rounded_close(eq_script.close)[0 if script.option_type == OptionType.CE else 1]))
            print("STRIKE: {}".format("STRIKE_PRICE"))
            print("Expiry: {}".format(script.expiry))
            print("Close: {}".format(script.close))
            print("LOT SIZE: {}".format(script.lot_size))
            print("ENTRY RANGE WITH TOLERANCE 0.5%: {}".format(trigger_range))
            print("SL: {}".format(sl))
            print("TARGET 1: {}".format(tgt1))
            print("TARGET 2: {}".format(tgt2))
            print("TARGET 3: {}".format(tgt3))
            print("CAPITAL REQUIRED FOR 1 LOT: {}".format(float(script.lot_size) * pcd))
            print("=====================================")

    def fetch_nfo_data(self):
        now = self.get_date()
        next_month = now + relativedelta.relativedelta(months=1)
        fno_data = list(
            filter(lambda x: x.instrument_type == "OPTSTK" and x.exchange == "NFO"
                             and ((now.month == x.expiry.month and now.year == x.expiry.year and now.day != x.expiry.day)
                                  or (next_month.month == x.expiry.month and next_month.year == x.expiry.year)),
                   self.alice.get_master_contract('NFO').values()))

        eq_set_keys = set()
        eq_set = set()
        for instrument in fno_data:
            if not instrument.eq in eq_set_keys:
                eq_set.add(instrument)
                eq_set_keys.add(instrument.eq)
        return fno_data, eq_set, fno_data[0].expiry

    def get_date(self):
        # date = input("Enter Date: ")
        # try:
        #     now = datetime.datetime.strptime(date, '%d-%m-%Y')
        # except:
        #     now = datetime.datetime.now()
        # return now
        return datetime.datetime.now()

    def _initialize_db(self):
        updated_nfo_data = []
        for instrument in self.eq_set:
            eq_instrument = self.alice.get_instrument_by_symbol("NSE", instrument.eq)
            eq_script = Script(eq_instrument, script_details=self.alice.get_scrip_info(eq_instrument))
            ce_instrument, ce_close, pe_instrument, pe_close = self.find_instruments(eq_script.symbol, eq_script.close)
            ce_script, pe_script = Script(ce_instrument, self.alice.get_scrip_info(ce_instrument),
                                          derived_from=ce_close), \
                                   Script(pe_instrument, self.alice.get_scrip_info(pe_instrument),
                                          derived_from=pe_close)
            update_script(eq_script)
            update_script(ce_script)
            update_script(pe_script)
            updated_nfo_data.append(ce_instrument)
            updated_nfo_data.append(pe_instrument)
        print("Scripts: " + str(len(Script.get_db()) // 3))
        self.nfo_data = updated_nfo_data

    def find_instruments(self, eq, close) -> tuple:
        ce_close, pe_close = self.get_rounded_close(close)
        return min(filter(lambda x: x.option_type == OptionType.CE.value and x.eq == eq, self.nfo_data),
                   key=lambda x: abs(x.strike_price - ce_close)), ce_close, \
               min(filter(lambda x: x.option_type == OptionType.PE.value and x.eq == eq, self.nfo_data),
                   key=lambda x: abs(x.strike_price - pe_close)), pe_close

    def get_rounded_close(self, value):
        return round_off(float(value) * (1 + 0.0075)), round_off(float(value) * (1 - 0.0075))

    def range_tolerance(self, value):
        value = round_off(value, 2)
        return [round_off(value * (1 - 0.005), 2), value, round_off(value * (1 + 0.0005), 2)]


def main():
    # pass
    print(datetime.datetime.now())
    we = WorkflowExecutor()
    we.execute()
    print(datetime.datetime.now())
    # print("Balance: " + str(we.alice.get_balance()))
    # alice.start_websocket(subscribe_callback=event_handler_quote_update)
    # alice.subscribe(alice.get_instrument_for_fno("AXISBANK", datetime.date(2022, 10, 27), False, "810.0", True), live_feed_type=LiveFeedType.TICK_DATA)
    # time.sleep(30)
    # import ipdb; ipdb.set_trace()
    # mc = we.alice.get_master_contract("NSE")
    # print(mc)
    # print("hi")


if __name__ == '__main__':
    main()
