import datetime
import time
import logging
from typing import Any

import position_management
from models import Script, Position
from position_management import PositionsManager
from variables import *
from constants import *
from utils import *

logger = logging.getLogger("Algorithm")


class Algorithm:

    def __init__(self, position_manager: PositionsManager):
        self.position_manager = position_manager

    def process(self, script: dict, square_off_in_progress: bool):
        if square_off_in_progress:
            return
        script = Script(instrument=script.get('instrument'), subscription_details=script)
        script = self.position_manager.update_script(script)
        script_lock = self.position_manager.get_or_create_script_lock(script.symbol)
        position_lock = self.position_manager.get_or_create_position_lock(script.symbol)
        try:
            script_lock.acquire()
            position_lock.acquire()
            if self.should_create_new_position(script):
                position = self.create_position(script)
                if position is not None:
                    logger.info("Entry: {}-{}, Close: {}, LTP: {}, OPEN: {}, HIGH: {}, LOW: {}, "
                                    "%CHNG: {}, Entry: {}".format(position.script.symbol,
                                                                             position.strategy.value,
                                                                             position.script.close,
                                                                             position.script.ltp,
                                                                             position.script.open,
                                                                             position.script.high,
                                                                             position.script.low,
                                                                             round_off((position.script.ltp - position.script.close) * 100 / position.script.close),
                                                                             position.entry_price))
                    print("Entry: {}-{}, Close: {}, LTP: {}, OPEN: {}, HIGH: {}, LOW: {}, "
                                    "%CHNG: {}, Entry: {}".format(position.script.symbol,
                                                                             position.strategy.value,
                                                                             position.script.close,
                                                                             position.script.ltp,
                                                                             position.script.open,
                                                                             position.script.high,
                                                                             position.script.low,
                                                                             round_off((position.script.ltp - position.script.close) * 100 / position.script.close),
                                                                             position.entry_price))
            else:
                position = self.update_position(script)
                if position is not None:
                    logger.info("Exit: {}-{}, Close: {}, LTP: {}, OPEN: {}, HIGH: {}, LOW: {}, "
                                    "%CHNG: {}, Entry: {}, Exit: {} ".format(position.script.symbol,
                                                                             position.strategy.value,
                                                                             position.script.close,
                                                                             position.script.ltp,
                                                                             position.script.open,
                                                                             position.script.high,
                                                                             position.script.low,
                                                                             round_off((position.script.ltp - position.script.close) * 100 / position.script.close),
                                                                             position.entry_price,
                                                                             position.exit_price))
                    print("Exit: {}-{}, Close: {}, LTP: {}, OPEN: {}, HIGH: {}, LOW: {}, "
                                    "%CHNG: {}, Entry: {}, Exit: {} ".format(position.script.symbol,
                                                                             position.strategy.value,
                                                                             position.script.close,
                                                                             position.script.ltp,
                                                                             position.script.open,
                                                                             position.script.high,
                                                                             position.script.low,
                                                                             round_off((position.script.ltp - position.script.close) * 100 / position.script.close),
                                                                             position.entry_price,
                                                                             position.exit_price))
        finally:
            position_lock.release()
            script_lock.release()

    def should_create_new_position(self, script: Script):
        now = datetime.datetime.now()
        if (now.hour*60 + now.minute) >= (14*60 + 10):
            return False
        elif script.ltp < MIN_OPTION_PRICE:
            return False
        elif self.position_manager.get_position(script):
            return False
        else:
            return True

    def create_position(self, script: Script):
        now = datetime.datetime.now()
        close = script.close
        ltp = script.ltp
        fail_low = round_off(close * (1 - 0.18), script.tick_size)

        if script.low >= close:
            # REGULAR
            entry = round_off(close * (1 + 0.095), script.tick_size)
            lower_end = entry - 2 * script.tick_size
            upper_end = entry + 2 * script.tick_size
            if lower_end <= ltp <= upper_end:
                position = Position(script, ltp, now, 1, Strategy.REGULAR)
                return self.position_manager.add_position(position)
        elif script.low >= fail_low:
            # REVISED 1
            entry = round_off(script.low * (1 + 0.1), script.tick_size)
            lower_end = entry - 2 * script.tick_size
            upper_end = entry + 2 * script.tick_size
            if lower_end <= ltp <= upper_end:
                position = Position(script, ltp, now, 1, Strategy.REVISED_1)
                return self.position_manager.add_position(position)
        else:
            # REVISED 2
            entry = round_off(script.low * (1 + 0.12), script.tick_size)
            lower_end = entry - 2 * script.tick_size
            upper_end = entry + 2 * script.tick_size
            if lower_end <= ltp <= upper_end:
                position = Position(script, ltp, now, 1, Strategy.REVISED_2)
                return self.position_manager.add_position(position)
        return None

    def update_position(self, script: Script):
        now = datetime.datetime.now()
        position = self.position_manager.get_position(script)
        if position is None or position.closed:
            return None
        ltp = script.ltp
        position.low = min(position.low, ltp)
        position.high = max(position.high, ltp)
        t1 = position.targets[0]
        t2 = position.targets[1]
        t3 = position.targets[2]
        sl = round_off(position.entry_price * (1 - 0.05), position.script.tick_size)

        if position.high >= t3 * (1 + 0.06):
            sl = round_off(position.high * (1 - 0.05), position.script.tick_size)
        elif position.high >= t3 * (1 + 0.01):
            sl = round_off(t3, position.script.tick_size)
        elif position.high >= t2 * (1 + 0.01):
            sl = round_off(t2, position.script.tick_size)
        elif position.high >= t1 * (1 + 0.01):
            sl = round_off(t1, position.script.tick_size)
        else:
            sl = round_off(position.entry_price * (1 - 0.05), position.script.tick_size)

        if ltp <= sl:
            self.close_position(position, ltp, now)
            return position

        return None

    def square_off(self):
        try:
            logger.info("Waiting for positions to close")
            print("Waiting for positions to close")
            time.sleep(20)
            now = datetime.datetime.now()
            position_mutex.acquire()
            for key in positions_db.keys():
                for position in positions_db[key].values():
                    if not position.closed:
                        self.close_position(position, position.script.ltp, now)
                        logger.info("Square Off: {} Close: {}, LTP: {}, OPEN: {}, HIGH: {}, LOW: {}, "
                                    "%CHNG: {}, Entry: {}, Exit: {} ".format(position.script.symbol,
                                                                             position.script.close,
                                                                             position.script.ltp,
                                                                             position.script.open,
                                                                             position.script.high,
                                                                             position.script.low,
                                                                             round_off((position.script.ltp - position.script.close) * 100/position.script.close),
                                                                             position.entry_price,
                                                                             position.exit_price))
                        print("Square Off: {} Close: {}, LTP: {}, OPEN: {}, HIGH: {}, LOW: {}, "
                                    "%CHNG: {}, Entry: {}, Exit: {} ".format(position.script.symbol,
                                                                             position.script.close,
                                                                             position.script.ltp,
                                                                             position.script.open,
                                                                             position.script.high,
                                                                             position.script.low,
                                                                             round_off((
                                                                                                   position.script.ltp - position.script.close) * 100 / position.script.close),
                                                                             position.entry_price,
                                                                             position.exit_price))
        finally:
            position_mutex.release()
    
    def close_position(self, position, price, now):
        if not position.closed:
            position.closed = True
            position.exit_price = price
            position.exit_time = now

    
