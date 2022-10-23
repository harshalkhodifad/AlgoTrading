def round_off(value, k=1):
    return round(value, k)


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
