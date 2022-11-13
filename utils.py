import datetime
import pickle


def round_off(value, precision=0.05):
    return round(round(value / precision) * precision, 2)


def convert_to_typ(typ, value):
    try:
        return typ(value)
    except:
        return None


def convert_to_int(value):
    return convert_to_typ(int, value)


def convert_to_float(value):
    return convert_to_typ(float, value)


def closest_value(input_list, input_value):
    return min(input_list, key=lambda il: abs(il - input_value))


def is_market_live() -> bool:
    now = datetime.datetime.now()
    time_in_seconds = now.hour * 3600 + now.minute * 60 + now.second
    if 1 <= now.isoweekday() <= 5:
        if 9*3600 + 15*60 <= time_in_seconds <= 15*3600 + 30*60:
            return True
    return False


def write_file(ds, name):
    f = open(name, "wb")
    pickle.dump(ds, f)
    f.close()


def read_file(name):
    f = open(name, "rb")
    ds = pickle.load(f)
    f.close()
    return ds


def write_csv(ds, name):
    csv_f = open(name, "w")
    csv_f.write("time,open,high,low,close,volume\n")
    for data in ds:
        csv_f.write(f"{data.time},{data.open},{data.high},{data.low},{data.close},{data.close}\n")
    csv_f.close()
