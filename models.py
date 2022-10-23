from __future__ import annotations
import string
from utils import convert_to_float, convert_to_int, round_off
from variables import *
from constants import *


class Script:

    def __init__(self, instrument, script_details=None, subscription_details=None, **kwargs):
        self.token = instrument.token
        self.exchange = instrument.exchange
        self.symbol = instrument.symbol
        self.name = instrument.name
        self.lot_size = instrument.lot_size
        self.expiry = instrument.expiry
        self.strike_price = convert_to_float(script_details.get('strikeprice') if script_details else subscription_details.get('strike_price'))
        self.ltp = convert_to_float(script_details.get('LTP') if script_details else subscription_details.get('ltp'))
        self.open = convert_to_float(script_details.get('openPrice') if script_details else subscription_details.get('open'))
        self.high = convert_to_float(script_details.get('High') if script_details else subscription_details.get('high'))
        self.low = convert_to_float(script_details.get('Low') if script_details else subscription_details.get('low'))
        self.close = convert_to_float(script_details.get('PrvClose') if script_details else subscription_details.get('close'))
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
    def add_or_update_script(script) -> Script:
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

    def __repr__(self):
        return f"Script: {self.__dict__}\n"
        # return f"Script: {self.symbol} {self.ltp}\n"


class Position:

    def __init__(self, symbol, entry_price, qty, strategy):
        self.symbol = symbol
        self.entry_price = entry_price
        self.qty = qty
        self.strategy = strategy
        self.exit_price = None
        self.closed = False

    @staticmethod
    def get_db():
        return positions_db

    @staticmethod
    def get_position(symbol: string):
        return positions_db[symbol]

    @staticmethod
    def add_position(position):
        Position.get_db()[position.symbol] = position

    @staticmethod
    def get_pnl():
        total_pnl = 0.00
        for position in positions_db.values():
            total_pnl += position.profit
        return total_pnl

    def close(self):
        self.closed = True
        self.exit_price = self.script.ltp

    @property
    def script(self) -> Script:
        return Script.get_script(self.symbol)

    @property
    def charges(self):
        return 50 * self.qty

    @property
    def profit(self):
        exit_price = self.exit_price if self.closed else self.script.ltp
        return round_off((exit_price - self.entry_price) * self.qty * self.script.lot_size - self.charges)

    def __repr__(self):
        return f"Position: {self.__dict__}\n"
        # return f"Position: {self.strategy.value} {self.symbol} {self.entry_price} {self.script.ltp} {self.profit}\n"
