import threading

position_mutex = threading.Lock()
positions_db = dict()
# {
#     "AXISBANK": {
#         "CE TICKER": Position
#     }
# }

position_locks = dict()

margin_mutex = threading.Lock()
script_mutex = threading.Lock()
current_margin = 0
max_margin = 0
scripts_db = dict()
script_locks = dict()
