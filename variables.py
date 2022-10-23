import threading

position_mutex = threading.Lock()
positions_db = dict()
position_locks = dict()

script_mutex = threading.Lock()
scripts_db = dict()
script_locks = dict()
