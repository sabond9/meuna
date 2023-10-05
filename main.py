import random
import time
import logging

from config import ACCOUNTS
from modules import Meuna, OpBNBBridge
from settings import RANDOM_WALLET, SLEEP_FROM, SLEEP_TO

# Configure logging to write errors to a log file
logging.basicConfig(filename='errors.log', level=logging.ERROR)

if __name__ == '__main__':
    if RANDOM_WALLET:
        random.shuffle(ACCOUNTS)

    for key in ACCOUNTS:
        try:
            bridge = OpBNBBridge(key)
            bridge.swap_to_opbnb()

            meuna = Meuna(key)
            meuna.start()

            time.sleep(random.randint(SLEEP_FROM, SLEEP_TO))
        except Exception as e:
            error_message = f"An error occurred for key '{key}': {str(e)}"
            logging.error(error_message)
