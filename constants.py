import enum
from collections import namedtuple

Credentials = namedtuple('Credentials', ['username', 'password', 'dob', 'app_secret', 'app_api_key'])

# Login CREDs
CREDS = [Credentials("720105",
                     "india18722",
                     "1234",
                     "XWovilUdgu7zQrW",
                     "sT0hgWxlQfJ4zK4iIfdHtApvc5VQyM1qSizHos5cDvXXedZK8gOMGrLXKHOi1m7t6DU7qiGP8t4IvulIZJgXv77a66j0PQHtCSL3")]

# General
QTY = 1
TOLERANCE = 0.01
RANGE_TOLERANCE_TICKS = 2
MIN_OPTION_PRICE = 5


# Option types
class OptionType(enum.Enum):
    CE = "CE"
    PE = "PE"


# Strategy
class Strategy(enum.Enum):
    REGULAR = "REGULAR"
    REVISED_1 = "REVISED_1"
    REVISED_2 = "REVISED_2"


class Exchanges(enum.Enum):
    NSE = "NSE"
    NFO = "NFO"
    MCX = "MCX"
