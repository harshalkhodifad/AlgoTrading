import time

from models import Script, Position
from variables import *
from constants import *


class Algorithm:

    def __init__(self):
        pass

    def process(self, script: Script):
        print(script)
        script = Script(instrument=script.get('instrument'), subscription_details=script)
        update_script(script)
        update_position(script)
    
