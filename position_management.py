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

    def get_position(self, script: Script) -> Position:
        return positions_db.get(script.eq_symbol, {}).get(script.symbol)

    def get_script(self, symbol) -> Script:
        return Script.get_script(symbol)

    def add_position(self, position: Position):
        positions_db[position.script.eq_symbol] = {
            position.script.symbol: position
        }
        return positions_db[position.script.eq_symbol][position.script.symbol]

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
