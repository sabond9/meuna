import random
import time

from loguru import logger

from config import DEPOSIT_OPBNB_ABI, DEPOSIT_OPBNB_CONTRACT
from modules import Account
from settings import BNB_RPC, MIN_GAS_VALUE


class OpBNBBridge(Account):
    def __init__(self, private_key: str) -> None:
        super().__init__(private_key=private_key, rpc=BNB_RPC)

    def get_tx_data(self):
        tx = {
            "chainId": self.w3.eth.chain_id,
            "from": self.address,
            "gasPrice": self.w3.eth.gas_price,
        }
        return tx

    def swap_to_opbnb(self):
        logger.info(f"[{self.address}] Swap to opBNB")

        contract = self.get_contract(DEPOSIT_OPBNB_CONTRACT, DEPOSIT_OPBNB_ABI)
        tx = self.get_tx_data()

        tx.update({"nonce": self.w3.eth.get_transaction_count(self.address)})

        transaction = contract.functions.depositETH(MIN_GAS_VALUE, b'').build_transaction(tx)

        signed_txn = self.sign(transaction)

        txn_hash = self.send_raw_transaction(signed_txn)

        self.wait_until_tx_finished(txn_hash.hex())

        time.sleep(random.randint(60, 70))
