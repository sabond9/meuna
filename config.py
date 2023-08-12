import json

with open("accounts.txt", "r") as file:
    ACCOUNTS = [row.strip() for row in file]

with open('data/erc20_abi.json') as file:
    ERC20_ABI = json.load(file)

with open('data/abi/faucet_abi.json') as file:
    FAUCET_ABI = json.load(file)

with open('data/abi/swap_abi.json') as file:
    ROUTER_ABI = json.load(file)

with open('data/abi/deposit_abi.json') as file:
    DEPOSIT_ABI = json.load(file)

with open('data/abi/short_abi.json') as file:
    SHORT_ABI = json.load(file)

FAUCET_CONTRACT = "0x67c03dBd6F8b377345D924726acDb5Eb5192F63E"

ROUTER_CONTRACT = "0x0970C29D31bFcd7ebF803B6C879B36f69fC39f28"

DEPOSIT_CONTRACT = "0x65cbe6bdc2b07b2e25ef6b53a97899fd4b4f1a8b"

SHORT_CONTRACT = "0xb45f6db83bbde9b6aa1dbc688b27c5c2defd6ad0"

HAY_ADDRESS = "0xA0C6843CCC4F4219e3e5751D4F93dE17C303D658"

MEUNA_TOKEN = "0x47034b3c18f17dd89ce1d7f87b9a90235158e4cc"

MEUNA_LP_TOKEN = "0xD7931924662D8086160B87D17622b23dFf04D129"
