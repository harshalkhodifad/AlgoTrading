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
        scrpt = Script(instrument=script.get('instrument'), subscription_details=script)
        script_lock = None
        now = datetime.datetime.now()
        try:
            global_lock.acquire()
            if now.second == 1:
                print("Running")
            script_lock = self.position_manager.get_or_create_script_lock(scrpt.symbol)
            script_lock.acquire()
            global_lock.release() if global_lock.locked() else None

            script = self.position_manager.update_script(scrpt)

            if self.should_create_new_position(script):
                self.create_position(script)
            else:
                self.update_position(script)

            script_lock.release() if script_lock.locked() else None
        except Exception as e:
            logger.error("Error occurred: ", e, exc_info=True)
        finally:
            script_lock.release() if script_lock.locked() else None
            global_lock.release() if global_lock.locked() else None

    def should_create_new_position(self, script: Script) -> bool:
        now = datetime.datetime.now()
        if (now.hour*60 + now.minute) >= (14*60 + 30):
            return False
        elif script.ltp < MIN_OPTION_PRICE:
            return False
        elif self.position_manager.get_position(script.symbol):
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
            lower_end = entry - RANGE_TOLERANCE_TICKS * script.tick_size
            upper_end = entry + RANGE_TOLERANCE_TICKS * script.tick_size
            if lower_end <= ltp <= upper_end:
                position = self.create_new_position(script, ltp, now, 1, Strategy.REGULAR)
                logger.info(position.summary)
                return position
        elif script.low >= fail_low:
            # REVISED 1
            entry = round_off(script.low * (1 + 0.10), script.tick_size)
            lower_end = entry - RANGE_TOLERANCE_TICKS * script.tick_size
            upper_end = entry + RANGE_TOLERANCE_TICKS * script.tick_size
            if lower_end <= ltp <= upper_end:
                position = self.create_new_position(script, ltp, now, 1, Strategy.REVISED_1)
                logger.info(position.summary)
                return position
        else:
            # REVISED 2
            entry = round_off(script.low * (1 + 0.12), script.tick_size)
            lower_end = entry - RANGE_TOLERANCE_TICKS * script.tick_size
            upper_end = entry + RANGE_TOLERANCE_TICKS * script.tick_size
            if lower_end <= ltp <= upper_end:
                position = self.create_new_position(script, ltp, now, 1, Strategy.REVISED_2)
                logger.info(position.summary)
                return position
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
        exit_reason = ""

        if position.high >= t3 * (1 + 0.06):
            sl = round_off(position.high * (1 - 0.05), position.script.tick_size)
            exit_reason = f"Achieved high of {position.high} after entry which is >= {t3 * (1 + 0.06)} " \
                          f"(t3({t3}) + 6%) and then price touched tsl(position high - 5%): {sl}"
        elif position.high >= t3 * (1 + 0.01):
            sl = round_off(t3, position.script.tick_size)
            exit_reason = f"Achieved high of {position.high} after entry which is >= {t3 * (1 + 0.01)} " \
                          f"(t3({t3}) + 1% tolerance) so, t3 became sl and price touched sl({sl})"
        elif position.high >= t2 * (1 + 0.01):
            sl = round_off(t2, position.script.tick_size)
            exit_reason = f"Achieved high of {position.high} after entry which is >= {t2 * (1 + 0.01)} " \
                          f"(t2({t2}) + 1% tolerance) so, t2 became sl and price touched sl({sl})"
        elif position.high >= t1 * (1 + 0.01):
            sl = round_off(t1, position.script.tick_size)
            exit_reason = f"Achieved high of {position.high} after entry which is >= {t1 * (1 + 0.01)} " \
                          f"(t1({t1}) + 1% tolerance) so, t1 became sl and price touched sl({sl})"
        else:
            sl = round_off(position.entry_price * (1 - 0.05), position.script.tick_size)
            exit_reason = f"Price touched hard sl(entry - 5%): {sl}"

        if ltp <= sl:
            self.close_position(position, ltp, now, exit_reason)
            logger.info(position.summary)
            return position

        return None

    def square_off(self):
        logger.info("Waiting for positions to close")
        print("Waiting for positions to close")
        time.sleep(5)
        now = datetime.datetime.now()
        positions = Position.get_db()
        for position in positions.values():
            if not position.closed:
                self.close_position(position, position.script.ltp, now, "Square Off")
                logger.info(position.summary)

    def create_new_position(self, script: Script, price: float, now: datetime.datetime, qty: int, stg: Strategy):
        p = Position(script, price, now, qty, stg)
        self.position_manager.add_position(p)
        try:
            global_lock.acquire()
            margin.current += p.margin
            margin.max = max(margin.current, margin.max)
            global_lock.release() if global_lock.locked() else None
        finally:
            global_lock.release() if global_lock.locked() else None
        return p

    @staticmethod
    def close_position(position, price, now, exit_reason):
        if not position.closed:
            position.closed = True
            position.exit_price = price
            position.exit_time = now
            position.exit_reason = exit_reason
            try:
                global_lock.acquire()
                margin.current += position.margin
                margin.max = max(margin.current, margin.max)
                global_lock.release() if global_lock.locked() else None
            finally:
                global_lock.release() if global_lock.locked() else None
            return position
