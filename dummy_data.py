import time
import datetime
from alice_blue import Instrument

data = {
    'AXISBANK22NOV880CE': [
# {'ml': '1', 'oi': '2806800', 'instrument': Instrument(exchange='NFO', instrument_type='OPTSTK', token=65556, symbol='AXISBANK22NOV910CE', eq='AXISBANK-EQ', name='AXISBANK 24NOV22 910 CE', option_type='CE', strike_price=910.0, expiry=datetime.date(2022, 11, 24), lot_size=1200), 'ltp': 6.65, 'percent_change': -8.28, 'change_value': 0, 'volume': 686400, 'open': 8.95, 'high': 8.95, 'low': 6.55, 'close': 7.25, 'exchange_time_stamp': datetime.datetime(2022, 11, 5, 15, 30, 8), 'atp': 7.39, 'tick_increment': 0.05, 'lot_size': 1200, 'best_bid_price': 6.6, 'best_ask_price': 6.65, 'best_bid_quantity': 1200, 'best_ask_quantity': 3600, 'price_precision': 2, 'total_open_interest': 0},
# {'ml': '1', 'oi': '2806800', 'instrument': Instrument(exchange='NFO', instrument_type='OPTSTK', token=65556, symbol='AXISBANK22NOV910CE', eq='AXISBANK-EQ', name='AXISBANK 24NOV22 910 CE', option_type='CE', strike_price=910.0, expiry=datetime.date(2022, 11, 24), lot_size=1200), 'ltp': 7, 'percent_change': -8.28, 'change_value': 0, 'volume': 686400, 'open': 8.95, 'high': 8.95, 'low': 6.55, 'close': 7.25, 'exchange_time_stamp': datetime.datetime(2022, 11, 5, 15, 30, 8), 'atp': 7.39, 'tick_increment': 0.05, 'lot_size': 1200, 'best_bid_price': 6.6, 'best_ask_price': 6.65, 'best_bid_quantity': 1200, 'best_ask_quantity': 3600, 'price_precision': 2, 'total_open_interest': 0}
    ],
    'AXISBANK22NOV870PE': [
{'ml': '1', 'oi': '2806800', 'instrument': Instrument(exchange='NFO', instrument_type='OPTSTK', token=65556, symbol='AXISBANK22NOV910CE', eq='AXISBANK-EQ', name='AXISBANK 24NOV22 910 CE', option_type='CE', strike_price=910.0, expiry=datetime.date(2022, 11, 24), lot_size=1200), 'ltp': 5, 'percent_change': -8.28, 'change_value': 0, 'volume': 686400, 'open': 8.95, 'high': 8.95, 'low': 6.55, 'close': 7.25, 'exchange_time_stamp': datetime.datetime(2022, 11, 5, 15, 30, 8), 'atp': 7.39, 'tick_increment': 0.05, 'lot_size': 1200, 'best_bid_price': 6.6, 'best_ask_price': 6.65, 'best_bid_quantity': 1200, 'best_ask_quantity': 3600, 'price_precision': 2, 'total_open_interest': 0},
{'ml': '1', 'oi': '2806800', 'instrument': Instrument(exchange='NFO', instrument_type='OPTSTK', token=65556, symbol='AXISBANK22NOV910CE', eq='AXISBANK-EQ', name='AXISBANK 24NOV22 910 CE', option_type='CE', strike_price=910.0, expiry=datetime.date(2022, 11, 24), lot_size=1200), 'ltp': 10, 'percent_change': -8.28, 'change_value': 0, 'volume': 686400, 'open': 8.95, 'high': 8.95, 'low': 6.55, 'close': 7.25, 'exchange_time_stamp': datetime.datetime(2022, 11, 5, 15, 30, 8), 'atp': 7.39, 'tick_increment': 0.05, 'lot_size': 1200, 'best_bid_price': 6.6, 'best_ask_price': 6.65, 'best_bid_quantity': 1200, 'best_ask_quantity': 3600, 'price_precision': 2, 'total_open_interest': 0},
{'ml': '1', 'oi': '2806800', 'instrument': Instrument(exchange='NFO', instrument_type='OPTSTK', token=65556, symbol='AXISBANK22NOV910CE', eq='AXISBANK-EQ', name='AXISBANK 24NOV22 910 CE', option_type='CE', strike_price=910.0, expiry=datetime.date(2022, 11, 24), lot_size=1200), 'ltp': 15, 'percent_change': -8.28, 'change_value': 0, 'volume': 686400, 'open': 8.95, 'high': 8.95, 'low': 6.55, 'close': 7.25, 'exchange_time_stamp': datetime.datetime(2022, 11, 5, 15, 30, 8), 'atp': 7.39, 'tick_increment': 0.05, 'lot_size': 1200, 'best_bid_price': 6.6, 'best_ask_price': 6.65, 'best_bid_quantity': 1200, 'best_ask_quantity': 3600, 'price_precision': 2, 'total_open_interest': 0},
{'ml': '1', 'oi': '2806800', 'instrument': Instrument(exchange='NFO', instrument_type='OPTSTK', token=65556, symbol='AXISBANK22NOV910CE', eq='AXISBANK-EQ', name='AXISBANK 24NOV22 910 CE', option_type='CE', strike_price=910.0, expiry=datetime.date(2022, 11, 24), lot_size=1200), 'ltp': 20, 'percent_change': -8.28, 'change_value': 0, 'volume': 686400, 'open': 8.95, 'high': 8.95, 'low': 6.55, 'close': 7.25, 'exchange_time_stamp': datetime.datetime(2022, 11, 5, 15, 30, 8), 'atp': 7.39, 'tick_increment': 0.05, 'lot_size': 1200, 'best_bid_price': 6.6, 'best_ask_price': 6.65, 'best_bid_quantity': 1200, 'best_ask_quantity': 3600, 'price_precision': 2, 'total_open_interest': 0}
    ]
}

l = max(list(map(len, data.values())))


def feed_dummy_data(callback):
    for i in range(l):
        for key in data.keys():
            if i < len(data[key]):
                callback(data[key][i])
        time.sleep(10)

