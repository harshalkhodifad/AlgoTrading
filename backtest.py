import configurations
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

test_instrument = Instrument("NFO", "OPTSTK", 65556, "AXISBANK22NOV910CE", "AXISBANK-EQ", "AXISBANK 24NOV22 910 CE", "CE", 910.0,
                                            datetime.date(2022, 11, 24), 1200)
# day
# fetch list -> if not available ignore
# one by one script
# multiple targets

logger = logging.getLogger("BACKTEST")
today = datetime.datetime(2022, 11, 4)
file_name = today.strftime("resources/backtest_data_%Y-%m-%d.pickle")
if os.path.isfile(file_name):
    # logger.info("Reading from file")
    scripts = read_file(file_name)
else:
    # logger.info("Fetching data")
    broker = Broker()
    yesterday = today - datetime.timedelta(days=3 if today.isoweekday() == 1 else 1)
    y_fr, y_to = yesterday + datetime.timedelta(hours=15, minutes=29), \
                                   yesterday + datetime.timedelta(hours=15, minutes=31)
    t_fr, t_to = today, today + datetime.timedelta(hours=15, minutes=45)
    fno_list, eqq_list, expiry = broker.get_nfo_data(today)
    eqq_list = list(eqq_list)

    for i, instrument in enumerate(eqq_list):
        logger.info("i: " + str(i))
        try:
            eq = broker.get_instrument_by_symbol("NSE", instrument.eq)
            eq_data = broker.get_historical_data(eq, y_fr, y_to)
            close = eq_data[-1].close
            derived_ce_close, derived_pe_close = float(close) * (1 + 0.0075), float(close) * (1 - 0.0075)
            ce_instrument = min(filter(lambda x: x.option_type == OptionType.CE.value and x.eq == eq.symbol, fno_list),
                       key=lambda x: abs(x.strike_price - derived_ce_close))
            pe_instrument = min(filter(lambda x: x.option_type == OptionType.PE.value and x.eq == eq.symbol, fno_list),
                       key=lambda x: abs(x.strike_price - derived_pe_close))
            ce_close = broker.get_historical_data(ce_instrument, y_fr, y_to)[-1].close
            pe_close = broker.get_historical_data(pe_instrument, y_fr, y_to)[-1].close
            ce_historical_data = broker.get_historical_data(ce_instrument, t_fr, t_to)
            pe_historical_data = broker.get_historical_data(pe_instrument, t_fr, t_to)
            data = BackTestScript(eq, ce_instrument, pe_instrument, close, ce_close, derived_ce_close, pe_close,
                                  derived_pe_close, ce_historical_data, pe_historical_data)
            scripts.update({eq.symbol: data})
        except Exception as e:
            logger.info(instrument)
            logger.info(e)
    write_file(scripts, file_name)

# logger.info(len(scripts))
# logger.info("Ended: {}".format(datetime.datetime.now()))
margin_used = 0


def exit_logic(script: BackTestScript, data: HistoricalData, last_candle: bool):
    global margin_used
    if script.active_position and data.low <= script.sl:
        script.active_position = False
        script.exit = script.sl
        script.exit_time = data.time
        margin_used += script.entry * script.lot
        logger.info(script)
        return True
    if script.active_position and script.targets[script.tg_i] <= data.high:
        if script.tg_i == 2:
            script.active_position = False
            script.exit = script.targets[script.tg_i]
            script.exit_time = data.time
            margin_used += script.entry * script.lot
            logger.info(script)
            return True
        if data.high >= script.targets[script.tg_i] * 1.05 and script.tg_i != 2:
            script.sl = script.targets[script.tg_i]
            script.tg_i += 1
    if script.active_position and last_candle:
        script.active_position = False
        script.exit = data.close
        script.exit_time = data.time
        margin_used += script.entry * script.lot
        logger.info(script)
        return True
    return False


def backtest_script(script: BackTestScript, ce: bool):
    close = script.ce_close if ce else script.pe_close
    historical_data = (script.ce_historical_data if ce else script.pe_historical_data)[10:-15]
    symbol = script.ce_instrument.symbol if ce else script.pe_instrument.symbol
    script.entry = None
    entry = close * (1 + 0.095)
    fail_low = close * (1 - 0.18)
    script.sl = entry * 0.95
    script.targets = [close * (1 + 0.16), close * (1 + 0.24), close * (1 + 0.35)]
    script.tg_i = 0
    is_first = True

    for i, data in enumerate(historical_data):
        script.day_low = min(script.day_low, data.low)
        script.day_high = max(script.day_high, data.high)
        if script.day_low < close:
            if script.day_low >= fail_low and not script.active_position:  # REVISED 1
                if not script.active_position and data.low <= script.day_low * 1.1 <= data.high:
                    if is_first:
                        is_first = False
                        continue
                    script.entry_type = "REVISED 1"
                    script.current_position_symbol = symbol
                    script.active_position = True
                    script.entry = script.day_low * 1.1
                    script.sl = script.entry * 0.95
                    script.entry_time = data.time
            if script.day_low < fail_low and not script.active_position:   # REVISED 2
                if not script.active_position and data.low <= script.day_low * 1.12 <= data.high:
                    if is_first:
                        is_first = False
                        continue
                    script.entry_type = "REVISED 2"
                    script.current_position_symbol = symbol
                    script.active_position = True
                    script.entry = script.day_low * 1.12
                    script.sl = script.entry * 0.95
                    script.entry_time = data.time
        else:   # REGULAR
            if not script.active_position and data.low <= entry <= data.high:
                if is_first:
                    is_first = False
                    continue
                script.entry_type = "REGULAR"
                script.current_position_symbol = symbol
                script.active_position = True
                script.entry = entry
                script.sl = script.entry * 0.95
                script.entry_time = data.time
        if script.active_position and exit_logic(script, data, len(historical_data) - 1 == i):
            break


i = 0
wins = 0
losses = 0
pnl = 0
for key in scripts.keys():
    i += 1
    script = scripts[key]
    # import ipdb; ipdb.set_trace()
    # bs = BackTestScript(script.instrument, script.ce_instrument, script.pe_instrument, script.eq_close,
    #                     script.ce_close, script.derived_ce_close, script.pe_close, script.derived_pe_close,
    #                     script.ce_historical_data, script.pe_historical_data)
    # scripts[key] = bs
    # write_file(scripts, file_name)
    backtest_script(script, True)
    if script.entry is not None:
        if script.pnl > 0:
            wins += 1
        else:
            losses += 1
        pnl += script.pnl
        continue
    backtest_script(script, False)
    if script.entry is not None:
        if script.pnl > 0:
            wins += 1
        else:
            losses += 1
        pnl += script.pnl

# logger.info("Wins: {}, Losses: {}, PNL: {}, Margin Used: {}, Gain: {}%".format(wins, losses, pnl, margin_used,
#                                                                           round_off(pnl*100/margin_used)))
logger.info("Wins: {}, Losses: {}, PNL: {}".format(wins, losses, round_off(pnl)))
print("Wins: {}, Losses: {}, PNL: {}".format(wins, losses, round_off(pnl)))


def main():
    pass


if __name__ == "__main__":
    main()

