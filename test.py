# %% test
from web3 import Web3
from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3 import Web3
from web3.middleware import construct_sign_and_send_raw_middleware
from uniswap import Uniswap
import logging
import sys

logging.basicConfig()

root = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)
root.setLevel(logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Starting")
logging.info("starting")

eth = "0x0000000000000000000000000000000000000000"
bat = "0x0D8775F648430679A709E98d2b0Cb6250d2887EF"
dai = "0x6B175474E89094C44Da98b954EedeAC495271d0F"

w3_provider = 'http://127.0.0.1:8545'
w3 = Web3(Web3.HTTPProvider(w3_provider))
myAddress = "0xf529310622238D948DAAb39Ab48A9eD694bF0015"
private_key = "0x0eb1d8afbe94c8032b4bf61117050ffec761435dec4b0d5efa315f9b305492ce"
poolAddress = "0x7379e81228514a1D2a6Cf7559203998E20598346"
assert private_key is not None, "You must set PRIVATE_KEY environment variable"
assert private_key.startswith("0x"), "Private key must start with 0x hex prefix"
account: LocalAccount = Account.from_key(private_key)
w3.middleware_onion.add(construct_sign_and_send_raw_middleware(account))
print(f"Your hot wallet address is {account.address}")
myAddress = account.address

# %%
uniswap = Uniswap(address=account.address, private_key=private_key, version=3, provider=w3_provider)


# %%
w3.eth.get_block('latest')

# %%
bal = w3.eth.get_balance(myAddress)
bal

# %%
bale = w3.fromWei(bal, 'ether')

# %%
t = w3.eth.get_transaction('0x3f64028c4eb41cb4976c4cf22d39533cd1bd97ac182cfb371407e4c0782963eb')
t
#type(t['input'])
#w3.fromWei(t['value'], 'ether')

# %%
w3.eth.get_balance(myAddress)

# %%
import math
def getPrice(sqrtPriceX96):
    temp = int(sqrtPriceX96 * sqrtPriceX96 * 1e18)
    return temp  >> (96 * 2)

def getPriceX96(wei):
    temp  = int(math.sqrt((wei << (96 * 2)) / (1e18)))
    return temp

getPrice(getPriceX96(1000000))

# %%
abi = open('abi/UniswapV3Pool.json').read()
# SETH2-ETH pool
pool = w3.eth.contract(address=poolAddress, abi=abi)
type(pool.functions.slot0().call()[0])
w3.fromWei(getPrice(pool.functions.slot0().call()[0]), 'ether')

# %%
abi = open('abi/Quoter.json').read()
quoter = w3.eth.contract(address="0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6", abi=abi)
res = quoter.functions.quoteExactInputSingle(
    "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
    "0xFe2e637202056d30016725477c5da089Ab0A043A",
    3000,
    w3.toWei(1, "ether"),
    0
).call()
w3.fromWei(res, 'ether')

# %%
addr =  w3.toChecksumAddress(myAddress)
t = pool.functions.swap(addr,
    True,
    w3.toWei(1, "ether"),
    getPriceX96(w3.toWei(1.02, "ether")),
    ""
    )
t.transact()
# %%
from web3.contract import ContractFunction
for f in pool.functions:
    print(f)
    print(pool.functions[f].arguments)

# %%
uniswap.make_trade(eth, dai, qty=w3.toWei(1, 'ether'), 
     recipient=myAddress, fee=3000)
# %%
