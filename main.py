import random
import time

from config import ACCOUNTS
from modules import Meuna, OpBNBBridge
from settings import RANDOM_WALLET, SLEEP_FROM, SLEEP_TO

if __name__ == '__main__':

    if RANDOM_WALLET:
        random.shuffle(ACCOUNTS)

    for key in ACCOUNTS:
        bridge = OpBNBBridge(key)
        bridge.swap_to_opbnb()

        meuna = Meuna(key)
        meuna.start()

        time.sleep(random.randint(SLEEP_FROM, SLEEP_TO))
