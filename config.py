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

with open('data/abi/deposit_op_bnb.json') as file:
    DEPOSIT_OPBNB_ABI = json.load(file)

FAUCET_CONTRACT = "0x5b8bff7becdf9fc0e656d65ba9c5382cf6a49087"

ROUTER_CONTRACT = "0x36550fF9a54fC5e1EFe0B1236e5f79df625D4bc2"

DEPOSIT_CONTRACT = "0xE1430cc4eAb91762435f7e20e8C1deB2c43C4940"

SHORT_CONTRACT = "0xeB664F1fA0F1D6F72552282B8650B1E11E592c38"

HAY_ADDRESS = "0x8e659c76791846cee0a33ccd741a0baec56c04dd"

MEUNA_TOKEN = "0xE660853bE6e0205966Ee1e38ad1e42609E5caAe9"

MEUNA_LP_TOKEN = "0x2b71db707f72ffd2d7c69c78963fe642a49360c3"

DEPOSIT_OPBNB_CONTRACT = "0x677311Fd2cCc511Bbc0f581E8d9a07B033D5E840"
