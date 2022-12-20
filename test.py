# %% test
from web3 import Web3
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# %%
w3.eth.get_block('latest')

# %%
bal = w3.eth.get_balance('0xf529310622238D948DAAb39Ab48A9eD694bF0015')
bal

# %%
bale = w3.fromWei(bal, 'ether')

# %%
t = w3.eth.get_transaction('0x3f64028c4eb41cb4976c4cf22d39533cd1bd97ac182cfb371407e4c0782963eb')
t
type(t['input'])
#w3.fromWei(t['value'], 'ether')

# %%
w3.eth.get_balance('0xB44a700dA3d7E0De2ca955A43BA71e0DeD44c96D')
# %%
from eth_abi import decode
decode(['uint256'], str.encode(t['input']))

# %%
def getPrice(sqrtPriceX96):
    temp = int(sqrtPriceX96 * sqrtPriceX96 * 1e18)
    return temp  >> (96 * 2)

# %%
abi = open('abi/UniswapV3Pool.json').read()
# SETH2-ETH pool
pool = w3.eth.contract(address="0x7379e81228514a1D2a6Cf7559203998E20598346", abi=abi)
type(pool.functions.slot0().call()[0])
getPrice(pool.functions.slot0().call()[0])

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
