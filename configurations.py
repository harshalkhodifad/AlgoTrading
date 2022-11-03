import logging
logging.basicConfig(filename='app-2022-11-01.txt', filemode='a', format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
# %(asctime)s -