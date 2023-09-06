import random
import time

from loguru import logger
from web3 import Web3
from config import FAUCET_CONTRACT, FAUCET_ABI, HAY_ADDRESS, MEUNA_TOKEN, ROUTER_CONTRACT, ROUTER_ABI, DEPOSIT_CONTRACT, \
    DEPOSIT_ABI, MEUNA_LP_TOKEN, SHORT_CONTRACT, SHORT_ABI
from settings import SLEEP_ACTION_FROM, SLEEP_ACTION_TO
from .account import Account


class Meuna(Account):
    def __init__(self, private_key: str) -> None:
        super().__init__(private_key=private_key)

        self.swap_contract = self.get_contract(ROUTER_CONTRACT, ROUTER_ABI)

    def get_tx_data(self):
        tx = {
            "chainId": self.w3.eth.chain_id,
            "from": self.address,
            "gasPrice": self.w3.eth.gas_price
        }
        return tx

    def mint_token(self):
        logger.info(f"[{self.address}] Mint tokens")

        contract = self.get_contract(FAUCET_CONTRACT, FAUCET_ABI)

        tx = self.get_tx_data()
        tx.update({"nonce": self.w3.eth.get_transaction_count(self.address)})

        transaction = contract.functions.claim().build_transaction(tx)

        signed_txn = self.sign(transaction)

        txn_hash = self.send_raw_transaction(signed_txn)

        self.wait_until_tx_finished(txn_hash.hex())

        time.sleep(random.randint(SLEEP_ACTION_FROM, SLEEP_ACTION_TO))

    def swap(self, from_token: str, to_token: str):
        balance = self.get_balance(from_token)
        amount = random.randint(int(balance["balance_wei"] * 0.1), int(balance["balance_wei"] * 0.6))

        logger.info(f"[{self.address}] Make swap")

        self.approve(amount, HAY_ADDRESS, ROUTER_CONTRACT)
        time.sleep(random.randint(5, 20))

        tx = self.get_tx_data()
        tx.update({"nonce": self.w3.eth.get_transaction_count(self.address)})

        transaction = self.swap_contract.functions.swapExactTokensForTokens(
            amount,
            0,
            [
                Web3.to_checksum_address(from_token),
                Web3.to_checksum_address(to_token),
            ],
            self.address,
            int(time.time()) + 1000000
        ).build_transaction(tx)

        signed_txn = self.sign(transaction)

        txn_hash = self.send_raw_transaction(signed_txn)

        self.wait_until_tx_finished(txn_hash.hex())

        receipts = self.w3.eth.get_transaction_receipt(txn_hash.hex())
        token_out = int(receipts["logs"][1]["data"].hex(), 0)

        time.sleep(random.randint(SLEEP_ACTION_FROM, SLEEP_ACTION_TO))

        return token_out

    def add_liquidity(self, from_token: str, to_token: str, amount: int):
        try:
            logger.info(f"[{self.address}] Add liquidity")

            amount_out = random.randint(int(amount * 0.1), int(amount * 0.6))

            liq_amount = self.swap_contract.functions.getAmountsIn(
                amount_out,
                [Web3.to_checksum_address(from_token),
                Web3.to_checksum_address(to_token)]
            ).call()

            self.approve(amount, MEUNA_TOKEN, ROUTER_CONTRACT)
            time.sleep(random.randint(5, 20))

            tx = self.get_tx_data()
            tx.update({"nonce": self.w3.eth.get_transaction_count(self.address)})

            transaction = self.swap_contract.functions.addLiquidity(
                Web3.to_checksum_address(from_token),
                Web3.to_checksum_address(to_token),
                liq_amount[0],
                liq_amount[1],
                0,
                0,
                self.address,
                int(time.time()) + 1000000
            ).build_transaction(tx)

            signed_txn = self.sign(transaction)

            txn_hash = self.send_raw_transaction(signed_txn)

            self.wait_until_tx_finished(txn_hash.hex())

            time.sleep(random.randint(SLEEP_ACTION_FROM, SLEEP_ACTION_TO))

        except Exception as e:
            print(e)
            self.add_liquidity(from_token, to_token, amount)

    def remove_liquidity(self, from_token: str, to_token: str):
        logger.info(f"[{self.address}] Remove liquidity")

        balance = self.get_balance(MEUNA_LP_TOKEN)

        self.approve(balance["balance_wei"], MEUNA_LP_TOKEN, ROUTER_CONTRACT)
        time.sleep(random.randint(5, 20))

        tx = self.get_tx_data()
        tx.update({"nonce": self.w3.eth.get_transaction_count(self.address)})

        transaction = self.swap_contract.functions.removeLiquidity(
            Web3.to_checksum_address(from_token),
            Web3.to_checksum_address(to_token),
            int(balance["balance_wei"] * 0.1),
            0,
            0,
            self.address,
            int(time.time()) + 1000000
        ).build_transaction(tx)

        signed_txn = self.sign(transaction)

        txn_hash = self.send_raw_transaction(signed_txn)

        self.wait_until_tx_finished(txn_hash.hex())

        time.sleep(random.randint(SLEEP_ACTION_FROM, SLEEP_ACTION_TO))

    def deposit(self):
        logger.info(f"[{self.address}] Make deposit")

        balance = self.get_balance(MEUNA_LP_TOKEN)
        amount = int(balance["balance_wei"] * 0.1)

        self.approve(balance["balance_wei"], MEUNA_LP_TOKEN, DEPOSIT_CONTRACT)
        time.sleep(random.randint(5, 20))

        tx = self.get_tx_data()
        tx.update({"nonce": self.w3.eth.get_transaction_count(self.address)})

        conract = self.get_contract(DEPOSIT_CONTRACT, DEPOSIT_ABI)

        transaction = conract.functions.deposit(
            0,
            amount
        ).build_transaction(tx)

        signed_txn = self.sign(transaction)

        txn_hash = self.send_raw_transaction(signed_txn)

        self.wait_until_tx_finished(txn_hash.hex())

        time.sleep(random.randint(SLEEP_ACTION_FROM, SLEEP_ACTION_TO))

        return amount

    def withdraw(self, amount):
        logger.info(f"[{self.address}] Make withdraw")

        amount = random.randint(int(amount*0.1), int(amount*0.5))

        self.approve(amount, MEUNA_LP_TOKEN, DEPOSIT_CONTRACT)
        time.sleep(random.randint(5, 20))

        tx = self.get_tx_data()
        tx.update({"nonce": self.w3.eth.get_transaction_count(self.address)})

        conract = self.get_contract(DEPOSIT_CONTRACT, DEPOSIT_ABI)

        transaction = conract.functions.withdraw(
            0,
            amount
        ).build_transaction(tx)

        signed_txn = self.sign(transaction)

        txn_hash = self.send_raw_transaction(signed_txn)

        self.wait_until_tx_finished(txn_hash.hex())

        time.sleep(random.randint(SLEEP_ACTION_FROM, SLEEP_ACTION_TO))

    def open_position(self, from_token: str, to_token: str, action: bool):
        logger.info(f"[{self.address}] Open position")

        balance = self.get_balance(HAY_ADDRESS)
        amount = random.randint(int(balance["balance_wei"] * 0.1), int(balance["balance_wei"] * 0.2))

        ration = Web3.to_wei(random.randint(150, 200), "ether")

        self.approve(amount, HAY_ADDRESS, SHORT_CONTRACT)
        time.sleep(random.randint(5, 20))
        self.approve(amount, MEUNA_TOKEN, SHORT_CONTRACT)
        time.sleep(random.randint(5, 20))

        tx = self.get_tx_data()
        tx.update({"nonce": self.w3.eth.get_transaction_count(self.address)})

        conract = self.get_contract(SHORT_CONTRACT, SHORT_ABI)

        transaction = conract.functions.openPosition(
            amount,
            Web3.to_checksum_address(to_token),
            Web3.to_checksum_address(from_token),
            ration,
            action
        ).build_transaction(tx)

        signed_txn = self.sign(transaction)

        txn_hash = self.send_raw_transaction(signed_txn)

        self.wait_until_tx_finished(txn_hash.hex())

        time.sleep(random.randint(SLEEP_ACTION_FROM, SLEEP_ACTION_TO))

    def start(self):
        self.mint_token()

        token_out = self.swap(HAY_ADDRESS, MEUNA_TOKEN)

        self.add_liquidity(MEUNA_TOKEN, HAY_ADDRESS, token_out)

        self.remove_liquidity(HAY_ADDRESS, MEUNA_TOKEN)

        dep_amount = self.deposit()

        self.open_position(HAY_ADDRESS, MEUNA_TOKEN, True)
        self.open_position(HAY_ADDRESS, MEUNA_TOKEN, False)

        self.withdraw(dep_amount)

        self.swap(MEUNA_TOKEN, HAY_ADDRESS)
