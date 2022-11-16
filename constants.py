import enum

# Login credentials - Trushar
# USERNAME = "720105"
# PASSWORD = "india18722"
# DOB = "1234"
# APP_SECRET = "XWovilUdgu7zQrW"
# APP_API_KEY = "sT0hgWxlQfJ4zK4iIfdHtApvc5VQyM1qSizHos5cDvXXedZK8gOMGrLXKHOi1m7t6DU7qiGP8t4IvulIZJgXv77a66j0PQHtCSL3"
# CHECKSUM = "35a3137016337bb27fb21ab15b9b5d81b6ce95f9647f585f40ff0bf62432eefa"
# AUTH_CODE = "TUB2ZY449SQA6I6RDLYU"
# SESSION_ID = "1uVstmmUbmh2X3fXlKfmH9jpvJayfZIrIbqF34z5OWLppD7ozzjiCLlIgmERhMEtpGQ4UcxSaFvKdGJ7JqdqFFWpH2Lshl4KhkkYPQU3BrtOHYgyLLeccqmZfMW8kfTqVGUVxFQIAHrCRTesSlbS4rfLfHFUBWxpUhN5AvrGXFkM8nGQBaDmZ3zVKOpdHqJqkcdDhpj4tZJraeBG4ddiefPOxmQp3aFPJnlu9LxinCEhUzEgxCcqDoEnzg7iL8dc"

# Login credential - HK
USERNAME = "722413"
PASSWORD = "Alice@22"
DOB = "1234"
APP_SECRET = "XUkELqxrJUGsQhg"
APP_API_KEY = "bXDSLDcKUnZbjmzLqRpvBdhQfAqBCENZLKquDbapoddmvMmDNiJOCzjutoMZSJCIpiLphaGXJAJjaoaTXqZVecerkAhFVmRRsglj"

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
