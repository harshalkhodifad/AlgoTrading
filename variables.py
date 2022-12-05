import threading

global_lock = threading.Lock()
script_locks = dict()

scripts_db = dict()
positions_db = dict()
position_archives = dict()


class Margin:

    def __init__(self):
        self.current = 0
        self.max = 0


margin = Margin()
