from AliceBlue_V2 import Alice, Instrument
import time

USER_ID = "720105"
API_KEY = "LvrQy3CFUHcjJs2yqZYojQb5deT2A9TIrX2vUtzhgjii5ueBq4nLQ4fJMVLjIIYrI3KAJBd9UQ7dSnDQY57Vyj7hN290FS3tPhlARkMSpeebZYLX5AbrZzmfidVTJz8U"

alice = Alice(user_id=USER_ID, api_key=API_KEY)
alice.create_session()
alice.download_master_contract("NSE", True)

socket_opened = False

def event_handler_quote_update(message):
    print(message)

def open_callback():
    global socket_opened
    socket_opened = True

# alice.invalidate_socket_session()
# alice.create_socket_session()
# alice.start_websocket(subscribe_callback=event_handler_quote_update,
#                       socket_open_callback=open_callback,
#                       run_in_background=True)
# while not socket_opened:
#     pass
# print("Websocket : Connected")
# alice.subscribe([alice.get_instrument_by_symbol("NSE", i) for i in ["NIFTY 50", "RELIANCE-EQ"]])
# time.sleep(60)

def main():
    # import ipdb; ipdb.set_trace()
    l = []
    ll = []
    # instrument = alice.get_instrument_by_symbol('NSE', 'NIFTY 50')
    # print(instrument)
    # l.append(time.time())
    # for i in range(1):
    #     ll.append(alice.get_scrip_details(instrument))
    # l.append(time.time())
    pass





if __name__ == '__main__':
    main()
