from __future__ import annotations

import datetime
import string
from typing import List
from alice_blue import Instrument

from utils import convert_to_float, convert_to_int, round_off, is_market_live
from variables import *
from constants import *


class Script:

    def __init__(self, instrument: Instrument, script_details=None, subscription_details=None, **kwargs):
        self.token = instrument.token
        self.exchange = instrument.exchange
        self.symbol = instrument.symbol
        self.name = instrument.name
        self.lot_size = instrument.lot_size
        self.expiry = instrument.expiry
        self.tick_size = convert_to_float(instrument.tick_size)
        self.strike_price = convert_to_float(script_details.get('strikeprice') if script_details else subscription_details.get('strike_price'))
        self.ltp = convert_to_float(script_details.get('LTP') if script_details else subscription_details.get('ltp'))
        self.open = convert_to_float(script_details.get('openPrice') if script_details else subscription_details.get('open'))
        self.high = convert_to_float(script_details.get('High') if script_details else subscription_details.get('high'))
        self.low = convert_to_float(script_details.get('Low') if script_details else subscription_details.get('low'))
        if is_market_live():
            self.close = convert_to_float(
                script_details.get('PrvClose') if script_details else subscription_details.get('close'))
        else:
            self.close = self.ltp
        self.volume = convert_to_int(script_details.get('TradeVolume') if script_details else subscription_details.get('volume'))
        self.bid = convert_to_float(None if script_details else subscription_details.get('best_bid_price'))
        self.ask = convert_to_float(None if script_details else subscription_details.get('best_ask_price'))
        self.bid_q = convert_to_int(None if script_details else subscription_details.get('best_bid_quantity'))
        self.ask_q = convert_to_int(None if script_details else subscription_details.get('best_ask_quantity'))
        self.price_precision = convert_to_int(script_details.get('DecimalPrecision') if script_details else subscription_details.get('price_precision'))
        self.instrument = instrument
        self.derived_from = kwargs.get("derived_from")

    @staticmethod
    def get_db():
        return scripts_db

    @staticmethod
    def add_or_update_script(script: Script) -> Script:
        if script.symbol in scripts_db:
            Script.get_script(script.symbol).__dict__.update({
                "ltp": script.ltp,
                "low": script.low,
                "high": script.high,
                "bid": script.bid,
                "ask": script.ask,
                "bid_q": script.bid_q,
                "ask_q": script.ask_q,
            })
            return Script.get_script(script.symbol)
        else:
            scripts_db[script.symbol] = script
        return script

    @staticmethod
    def get_script(symbol) -> Script:
        return scripts_db.get(symbol)

    @property
    def eq_symbol(self):
        return self.instrument.name.split(" ")[0] + "-EQ" if not self.instrument.symbol.endswith('-EQ') \
            else self.instrument.symbol

    @property
    def eq_script(self):
        return scripts_db.get(self.eq_symbol)

    @property
    def option_type(self):
        if self.instrument.symbol.endswith(OptionType.CE.value):
            return OptionType.CE
        elif self.instrument.symbol.endswith(OptionType.PE.value):
            return OptionType.PE
        else:
            return None

    @property
    def change_percentage(self):
        return round((self.ltp - self.close) * 100 / self.close, 2)

    def __repr__(self):
        return f"Script: {self.__dict__}\n"
        # return f"Script: {self.symbol} {self.ltp}\n"


class Position:

    def __init__(self, script: Script, entry_price, entry_time: datetime.datetime, qty, strategy: Strategy):
        self.script = script
        self.low = entry_price
        self.high = entry_price
        self.entry_price = entry_price
        self.entry_time = entry_time
        self.entry_reason = ""
        self.exit_price = None
        self.exit_time = None
        self.exit_reason = ""
        self.qty = qty
        self.strategy = strategy
        self.closed = False

    @staticmethod
    def get_db():
        return positions_db

    @staticmethod
    def get_position(symbol: string):
        return positions_db.get(symbol)

    @staticmethod
    def add_position(position):
        Position.get_db()[position.symbol] = position

    @property
    def gross_pnl(self):
        return round((self.exit_price - self.entry_price) * self.script.lot_size * self.qty, 2)

    @property
    def margin(self) -> float:
        return self.qty * self.entry_price * self.script.lot_size

    @property
    def charges(self):
        return 40 * self.qty

    @property
    def profit(self):
        exit_price = self.exit_price if self.closed else self.script.ltp
        return round_off((exit_price - self.entry_price) * self.qty * self.script.lot_size - self.charges)

    @property
    def targets(self):
        return [round_off(self.entry_price * 1.16, self.script.tick_size),
                round_off(self.entry_price * 1.24, self.script.tick_size),
                round_off(self.entry_price * 1.35, self.script.tick_size)]

    @property
    def sl(self) -> float:
        return 0.0

    @property
    def summary(self):
        if not self.closed:
            return f"{self.strategy.value} Entry {self.script.symbol} - Entry Price: {self.entry_price}, " \
                   f"CLOSE: {self.script.close}, OPEN: {self.script.open}, LOW: {self.script.low}, " \
                   f"HIGH: {self.script.high}, %CHANGE: {self.script.change_percentage}, " \
                   f"LOT: {self.script.lot_size}, MARGIN USED: {self.margin}\n"
        else:
            return f"{self.strategy.value} Exit {self.script.symbol} - Gross PnL: {self.gross_pnl}, " \
                   f"Entry Price: {self.entry_price}, Exit Price: {self.exit_price}, OPEN: {self.script.open}, " \
                   f"LOW: {self.script.low}, HIGH: {self.script.high}, %CHANGE: {self.script.change_percentage}, " \
                   f"LOT: {self.script.lot_size}, MARGIN USED: {self.margin}, Reason: {self.exit_reason}\n"

    def __repr__(self):
        return f"Position: {self.__dict__}\n"


class HistoricalData:

    def __init__(self, data):
        #import ipdb; ipdb.set_trace()
        # {'volume': 2400.0, 'high': 32.3, 'low': 32.3, 'time': '2022-10-27 15:30:59', 'close': 32.3, 'open': 32.3}
        self.high = convert_to_float(data.get('high'))
        self.low = convert_to_float(data.get('low'))
        self.open = convert_to_float(data.get('open'))
        self.close = convert_to_float(data.get('close'))
        self.volume = convert_to_float(data.get('volume'))
        self.time = datetime.datetime.strptime(data.get('time'), '%Y-%m-%d %H:%M:%S')

    def __repr__(self):
        #return ""
        return f"HistoricalData: {self.__dict__}"


class BackTestScript:

    def __init__(self, instrument: Instrument,
                 ce_instrument: Instrument,
                 pe_instrument: Instrument,
                 eq_close: float,
                 ce_close: float,
                 derived_ce_close: float,
                 pe_close: float,
                 derived_pe_close: float,
                 ce_historical_data: List[HistoricalData],
                 pe_historical_data: List[HistoricalData]):
        self.instrument = instrument
        self.ce_instrument = ce_instrument
        self.pe_instrument = pe_instrument
        self.ce_historical_data = ce_historical_data
        self.pe_historical_data = pe_historical_data
        self.eq_close = eq_close
        self.ce_close = ce_close
        self.pe_close = pe_close
        self.derived_ce_close = derived_ce_close
        self.derived_pe_close = derived_pe_close
        self.lot = ce_instrument.lot_size
        self.active_position = False
        self.current_position_symbol = ""
        self.entry_type = ""
        self.day_low = 100000000
        self.day_high = -1
        self.entry = None
        self.sl = None
        self.entry_time = None
        self.exit = None
        self.exit_time = None
        self.targets = []
        self.tg_i = 0

    @property
    def pnl(self):
        return (self.exit - self.entry) * self.lot

    def __repr__(self):
        # return f"BackTestScript: {self.__dict__} PNL: {self.pnl}"
        # return "{} Symbol:{}, PnL:{}, entry time:{}, entry:{}, exit time:{}, exit:{} || SL: {}, Targets: {}\n\n"\
        #     .format(self.entry_type, self.current_position_symbol, round_off(self.pnl),
        #             self.entry_time.strftime("%H:%M:%S"), round_off(self.entry),
        #             self.exit_time.strftime("%H:%M:%S"), round_off(self.exit), round_off(self.sl), list(map(round_off, self.targets)))
        return "Symbol:{}, PnL:{}, entry time:{}, entry:{}, exit time:{}, exit:{}" \
            .format(self.current_position_symbol, round_off(self.pnl),
                    self.entry_time.strftime("%H:%M:%S"), round_off(self.entry),
                    self.exit_time.strftime("%H:%M:%S"), round_off(self.exit))
