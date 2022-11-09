print("Balance: " + str(we.alice.get_balance()))
alice.start_websocket(subscribe_callback=event_handler_quote_update)
alice.subscribe(alice.get_instrument_for_fno("AXISBANK", datetime.date(2022, 10, 27), False, "810.0", True), live_feed_type=LiveFeedType.TICK_DATA)
time.sleep(30)
import ipdb; ipdb.set_trace()
mc = we.alice.get_master_contract("NSE")
print("hi")

alice = Alice(USERNAME, "APP_SECRET")
alice.session_id = AliceBlue.login_and_get_sessionID(username=USERNAME,
                                                     password=PASSWORD,
                                                     twoFA=DOB,
                                                     app_id=APP_API_KEY,
                                                     api_secret=APP_SECRET)
# print(alice.create_session())  # Must "log in" to Alice platform before create session
alice.download_master_contract(False)  # Download initially once a day
print(alice.get_profile())

algo = Algo()

self.alice.start_websocket(subscriber_callback)
        self.alice.subscribe(self.nfo_data, LiveFeedType.TICK_DATA)
        time.sleep(20)
        self.alice.subscribe([self.alice.get_instrument_by_symbol("NSE", "AXISBANK-EQ")], LiveFeedType.TICK_DATA)
        SILVERM22NOVFUT
        self.alice.unsubscribe([self.alice.get_instrument_by_symbol("NSE", "AXISBANK22OCT810CE")], LiveFeedType.TICK_DATA)
        self.alice.close_websocket()

        self.alice.invalidate_socket_session()
        self.alice.create_socket_session()
        self.alice.start_websocket(subscribe_callback=event_handler_quote_update,
                                   socket_open_callback=open_callback,
                                   run_in_background=True)
        while not socket_opened:
            pass
        print("Websocket : Connected")
        self.alice.subscribe(
            [self.alice.get_instrument_by_symbol("NFO", i) for i in ["AXISBANK22OCT810CE", "AXISBANK22OCT810PE"]])
        time.sleep(600)

for instrument in self.nfo_data:
    script = Script.get_script(instrument.symbol)
    eq_script = Script.get_script(script.eq_symbol)

    # print(entity)
    pc = script.ltp
    ltp = script.ltp
    pcd = round_off(pc * (1 + 0.095))
    trigger_range = self._range_tolerance(pcd)
    sl = round_off(pcd * (1 - 0.05))
    tgt1 = round_off(pcd * (1 + 0.16))
    tgt2 = round_off(pcd * (1 + 0.24))
    tgt3 = round_off(pcd * (1 + 0.35))

    if ltp < 5.00:
        print("Ignoring script: {} as price {} is below 5".format(script.symbol, ltp))
        continue

    print("=============REGULAR BUY=============")
    print("NAME: {}".format(script.symbol))
    print("EQ CLOSE: {}".format(eq_script.ltp))
    print("EQ DERIVED CLOSE: {}".format(
        self.get_rounded_close(eq_script.close)[0 if script.option_type == OptionType.CE else 1]))
    print("STRIKE: {}".format(script.strike_price))
    print("Expiry: {}".format(script.expiry))
    print("Close: {}".format(script.ltp))
    print("LOT SIZE: {}".format(script.lot_size))
    print("ENTRY RANGE WITH TOLERANCE 0.5%: {}".format(trigger_range))
    print("SL: {}".format(sl))
    print("TARGET 1: {}".format(tgt1))
    print("TARGET 2: {}".format(tgt2))
    print("TARGET 3: {}".format(tgt3))
    print("CAPITAL REQUIRED FOR 1 LOT: {}".format(float(script.lot_size) * pcd))
    print("=====================================")