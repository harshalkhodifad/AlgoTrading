import logging
import threading

from models import Script, Position
from variables import positions_db, position_mutex, position_locks, scripts_db, script_mutex, script_locks
from constants import QTY, Strategy

# Global variables
logger = logging.getLogger("PositionsManager")


class PositionsManager:

    def __init__(self):
        pass

    def init_position_locks(self):
        for symbol in script_locks:
            self.get_or_create_position_lock(symbol)

    def update_position(self, script: Script):
        position_lock = self.get_or_create_position_lock(script.symbol)
        try:
            position_lock.acquire(True)
            if script.symbol in positions_db:
                self.close_or_update_position(script)
            else:
                self.create_position(script)
        finally:
            position_lock.release()

    def get_position(self, script: Script):
        position_lock = self.get_or_create_position_lock(script.symbol)
        try:
            position_lock.acquire(True)
            return positions_db.get(script.eq_symbol, {}).get(script.symbol)
        finally:
            position_lock.release()

    def close_or_update_position(self, script: Script):
        p = Position.get_position(script.symbol)
        print(p)

    def create_position(self, script: Script):
        p = Position(script.symbol, script.ltp, QTY, Strategy.REGULAR)
        Position.add_position(p)

    def update_script(self, script: Script) -> Script:
        script_lock = self.get_or_create_script_lock(script.symbol)
        try:
            script_lock.acquire(True)
            return Script.add_or_update_script(script)
        finally:
            script_lock.release()

    def get_or_create_position_lock(self, symbol) -> threading.Lock:
        try:
            position_mutex.acquire(True)
            if symbol not in position_locks:
                position_locks[symbol] = threading.Lock()
            return position_locks[symbol]
        finally:
            position_mutex.release()

    def get_or_create_script_lock(self, symbol) -> threading.Lock:
        try:
            script_mutex.acquire(True)
            if symbol not in script_locks:
                script_locks[symbol] = threading.Lock()
            return script_locks[symbol]
        finally:
            script_mutex.release()
