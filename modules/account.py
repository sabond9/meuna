import time
import random

from loguru import logger
from web3 import Web3
from eth_account import Account as EthereumAccount
from web3.exceptions import TransactionNotFound

from config import ERC20_ABI
from settings import OP_RPC


class Account:
    def __init__(self, private_key: str, rpc: str) -> None:
        self.private_key = private_key
        self.explorer = "https://testnet.bscscan.com/tx/"

        self.w3 = Web3(Web3.HTTPProvider(rpc))
        self.account = EthereumAccount.from_key(private_key)
        self.address = self.account.address

    def get_contract(self, token_address: str, abi=None):
        token_address = Web3.to_checksum_address(token_address)

        if abi is None:
            abi = ERC20_ABI

        contract = self.w3.eth.contract(address=token_address, abi=abi)

        return contract

    def get_balance(self, token_address=None):
        contract = self.get_contract(token_address)

        symbol = contract.functions.symbol().call()
        decimal = contract.functions.decimals().call()
        balance_wei = contract.functions.balanceOf(self.address).call()

        balance = balance_wei / 10 ** decimal

        return {"balance_wei": balance_wei, "balance": balance, "symbol": symbol, "decimal": decimal}

    def check_allowance(self, token_address: str, contract_address: str) -> float:
        contract = self.w3.eth.contract(address=token_address, abi=ERC20_ABI)
        amount_approved = contract.functions.allowance(self.address, contract_address).call()

        return amount_approved

    def approve(self, amount: float, token_address: str, contract_address: str):
        token_address = Web3.to_checksum_address(token_address)
        contract_address = Web3.to_checksum_address(contract_address)
        contract = self.w3.eth.contract(address=token_address, abi=ERC20_ABI)

        allowance_amount = self.check_allowance(token_address, contract_address)

        if amount > allowance_amount:
            logger.success(f"[{self.address}] approve is successfully!")

            tx = {
                "chainId": self.w3.eth.chain_id,
                "from": self.address,
                "nonce": self.w3.eth.get_transaction_count(self.address),
                "gasPrice": self.w3.eth.gas_price
            }
            transaction = contract.functions.approve(
                contract_address,
                100000000000000000000000000000000000000000000000000000000000000000000000000000
            ).build_transaction(tx)

            signed_txn = self.sign(transaction)
            txn_hash = self.send_raw_transaction(signed_txn)
            self.wait_until_tx_finished(txn_hash.hex())

    def wait_until_tx_finished(self, hash: str, max_wait_time=180):
        start_time = time.time()
        while True:
            try:
                receipts = self.w3.eth.get_transaction_receipt(hash)
                status = receipts.get("status")
                if status == 1:
                    logger.success(f"[{self.address}] {self.explorer}{hash} successfully!")

                    return True
                elif status is None:
                    time.sleep(0.3)
                elif status != 1:
                    logger.error(f"[{self.address}] {self.explorer}{hash} transaction failed!")

                    return False
            except TransactionNotFound:
                if time.time() - start_time > max_wait_time:
                    print(f'FAILED TX: {hash}')

                    return False
                time.sleep(1)

    def sign(self, transaction):
        signed_txn = self.w3.eth.account.sign_transaction(transaction, self.private_key)

        return signed_txn

    def send_raw_transaction(self, signed_txn):
        txn_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)

        return txn_hash
