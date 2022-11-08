import logging
import datetime
from typing import List

from alice_blue import AliceBlue, Instrument
from alice_blue import LiveFeedType, HistoricalDataType

from models import Script, HistoricalData
from utils import round_off
import csv
import time
from dateutil import relativedelta

from constants import *

logger = logging.getLogger(__name__)


class Broker:

    def __init__(self):
        self.client = AliceClient()

    def get_script_info(self, eq_instrument) -> Script:
        script_details = self.client.get_script_info(eq_instrument)
        # print(script_details)
        logger.info(script_details)
        return Script(eq_instrument, script_details=self.client.get_script_info(eq_instrument))

    def get_instrument_by_symbol(self, exch, symbol):
        return self.client.get_instrument_by_symbol(exch, symbol)

    def get_nfo_data(self, now):
        next_month = now + relativedelta.relativedelta(months=1)
        fno_data = list(
            filter(lambda x: x.instrument_type == "OPTSTK" and x.exchange == "NFO" and x.symbol.startswith('AX')
                             and ((
                                              now.month == x.expiry.month and now.year == x.expiry.year and now.day != x.expiry.day)
                                  or (next_month.month == x.expiry.month and next_month.year == x.expiry.year)),
                   self.client.get_master_contract('NFO').values()))

        eq_set_keys = set()
        eq_set = set()
        for instrument in fno_data:
            if not instrument.eq in eq_set_keys:
                eq_set.add(instrument)
                eq_set_keys.add(instrument.eq)
        return fno_data, eq_set, fno_data[0].expiry

    def get_historical_data(self, instrument, fr, to) -> List[HistoricalData]:
        l = self.client.historical_data(instrument, fr, to, HistoricalDataType.Minute).get('result')
        ll = []
        for x in l:
            ll.append(HistoricalData(x))
        return ll

    def subscribe(self, instruments: List[Instrument], callback_fn):
        self.client.subscribe_instruments(instruments, callback_fn)

    def unsubscribe(self, instruments: List[Instrument]):
        self.client.unsubscribe_instruments(instruments)


class AliceClient(AliceBlue):

    def __init__(self):
        super().__init__(username=USERNAME, session_id=AliceBlue.login_and_get_sessionID(username=USERNAME,
                                                                                         password=PASSWORD,
                                                                                         twoFA=DOB,
                                                                                         app_id=APP_SECRET,
                                                                                         api_secret=APP_API_KEY))

    def subscribe_instruments(self, instruments: List[Instrument], callback_fn):
        self.start_websocket(subscribe_callback=callback_fn)
        self.subscribe(instruments, LiveFeedType.TICK_DATA)

    def unsubscribe_instruments(self, instruments):
        self.unsubscribe(instruments, LiveFeedType.TICK_DATA)
