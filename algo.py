import time

from models import Script, Position
from variables import *
from constants import *


def subscriber_callback(script):
    print(script)
    script = Script(instrument=script.get('instrument'), subscription_details=script)
    update_script(script)
    update_position(script)
    # print(Script.get_db())
    # time.sleep(5)


def update_position(script: Script):
    position_lock = get_or_create_position_lock(script.symbol)
    try:
        position_lock.acquire(True)
        if script.symbol in positions_db:
            close_or_update_position(script)
        else:
            create_position(script)
    finally:
        position_lock.release()


def close_or_update_position(script: Script):
    p = Position.get_position(script.symbol)
    print(p)


def create_position(script: Script):
    p = Position(script.symbol, script.ltp, QTY, Strategy.REGULAR)
    Position.add_position(p)


def update_script(script: Script):
    script_lock = get_or_create_script_lock(script.symbol)
    try:
        script_lock.acquire(True)
        Script.add_or_update_script(script)
    finally:
        script_lock.release()


def get_or_create_position_lock(symbol) -> threading.Lock:
    try:
        position_mutex.acquire(True)
        if symbol not in position_locks:
            position_locks[symbol] = threading.Lock()
        return position_locks[symbol]
    finally:
        position_mutex.release()


def get_or_create_script_lock(symbol) -> threading.Lock:
    try:
        script_mutex.acquire(True)
        if symbol not in script_locks:
            script_locks[symbol] = threading.Lock()
        return script_locks[symbol]
    finally:
        script_mutex.release()
