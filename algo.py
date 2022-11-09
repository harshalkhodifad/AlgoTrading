import datetime
import time

import position_management
from models import Script, Position
from position_management import PositionsManager
from variables import *
from constants import *


class Algorithm:

    def __init__(self, position_manager: PositionsManager):
        self.position_manager = position_manager

    def process(self, script: dict, square_off_in_progress: bool):
        if square_off_in_progress:
            return
        print(script)
        script = Script(instrument=script.get('instrument'), subscription_details=script)
        script = self.position_manager.update_script(script)
        print(script)
        if self.should_create_new_position(script):
            self.create_position(script)
        else:
            self.update_position(script)
        # update_script(script)
        # update_position(script)

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

    def update_position(self, script: Script):
        pass
    
