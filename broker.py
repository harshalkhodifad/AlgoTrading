def get_instrument_for_fno(self, exchange, name, expiry_date, is_fut=True, strike=None, is_CE=False):
    if self.master_contract is None:
        raise Exception("Download Master Contract First")
    contract = self.master_contract[self.master_contract['exchange'] == exchange]
    contract = contract[contract["name"] == name]
    contract = contract[contract["expiry"] == expiry_date]
    contract = contract[contract["instrument_type"] == ("XX" if bool(is_fut) else ("CE" if bool(is_CE) else "PE"))]
    if strike is not None and not bool(is_fut):
        contract = contract[contract["strike"] == float(strike)]
    if len(contract) == 0 or len(contract) > 1:
        raise Exception("Provide valid data")
    return Instrument(list(contract['exchange'])[0], list(contract['instrument_token'])[0],
                      list(contract['trading_symbol'])[0], list(contract['name'])[0],
                      list(contract['expiry'])[0], list(contract['lot_size'])[0])


def get_historical(self, instrument, from_datetime, to_datetime, interval, indices=False):
    # intervals = ["1", "2", "3", "4", "5", "10", "15", "30", "60", "120", "180", "240", "D", "1W", "1M"]
    params = {"symbol": instrument.token,
              "exchange": instrument.exchange if not indices else f"{instrument.exchange}::index",
              "from": str(int(from_datetime.timestamp())),
              "to": str(int(to_datetime.timestamp())),
              "resolution": interval,
              "user": self.user_id}
    lst = requests.get(
        f"https://a3.aliceblueonline.com/rest/AliceBlueAPIService/chart/history?", params=params).json()
    df = pd.DataFrame(lst)
    df = df.rename(columns={'t': 'datetime', 'o': 'open', 'h': 'high', 'l': 'low', 'c': 'close', 'v': 'volume'})
    df = df[['datetime', 'open', 'high', 'low', 'close', 'volume']]
    df["datetime"] = df["datetime"].apply(lambda x: datetime.datetime.fromtimestamp(x))
    return df

    def get_master_contract(self, exchange=None):
        if self.master_contract is None:
            try:
                self.master_contract = pd.read_csv("Exchange.csv")
                self.master_contract["expiry"] = self.master_contract["expiry"].apply(
                    lambda x: dateutil.parser.parse(str(x)).date() if str(x).strip() != "nan" and bool(x) else x)
            except:
                self.download_master_contract()
        if exchange is None:
            return self.master_contract
        else:
            contract = self.master_contract[self.master_contract['exchange'] == exchange]
            if len(contract) == 0:
                raise Exception("Provide valid data")
            else:
                return contract