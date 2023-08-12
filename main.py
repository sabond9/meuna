import random
import time

from config import ACCOUNTS
from modules import Meuna
from settings import RANDOM_WALLET, SLEEP_FROM, SLEEP_TO

if __name__ == '__main__':
    print("\n\nSubscribe to me –– https://t.me/sybilwave\n")

    if RANDOM_WALLET:
        random.shuffle(ACCOUNTS)

    for key in ACCOUNTS:
        meuna = Meuna(key)
        meuna.start()

        time.sleep(random.randint(SLEEP_FROM, SLEEP_TO))

