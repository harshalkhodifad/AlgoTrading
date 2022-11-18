import logging
import datetime
now = datetime.datetime.now()
logger_file = now.strftime("logs/algo-trading-%Y-%m-%d.txt")
logging.basicConfig(filename=logger_file, filemode='a', format='%(name)s - %(levelname)s - %(asctime)s - %(message)s',
                    level=logging.INFO)
