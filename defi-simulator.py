# A simulator to predict defi markets
from src.chain.Pool import Pool
from src.chain.blockchain import BlockChain
from src.chain.pojos import Token, Wallet, Block
from src.chain.transactions.AccountToAccount import AccountToAccount
from src.chain.transactions.CompositeSwap import SwapPath, CompositeSwap
from src.chain.transactions.Swap import Swap
from src.chain.transactions.liquidity import AddLiquidity, RemoveLiquidity
from src.simulations.BBBEffect import BBBEffectSimulation
from src.strategies.cexArbStrat import cexArbStrat
from src.strategies.oracleStrat import OracleFromLambda

print("loading simulation")
# current: 120e3 30e3
sim = BBBEffectSimulation(sellsPerDay=50e3,buysPerDay=50e3,ratioToDFI=0.8,BBBDFIPerDay=110e3)

sim.initChain()

# run 30 days
print(f"per day: {sim.buysPerDay:.0f} buys, {sim.sellsPerDay:.0f} sells, {sim.ratioToDFI*100}% to DFI, {'with BBB' if sim.BBBDFIPerDay > 0 else 'without BBB'}")
print(f"day\tDFI\tDUSD via stable\tDUSD via DFI")

sim.run(2880*90)
dfiprice = sim.chain.pools["USDT-DFI"].getSwapValueAfterFees(False)
dusdstable = sim.chain.pools["USDT-DUSD"].getSwapValueAfterFees(False)
dusdViaDFI = CompositeSwap.calcPriceOnPath(
        SwapPath([sim.chain.pools["USDT-DFI"], sim.chain.pools["DUSD-DFI"]], "USDT", "DUSD"))
print(f"{90}\t{dfiprice:.4f}\t{dusdstable:.2f}\t{dusdViaDFI:.2f}")

'''
def oraclePrice(poolId:str, chain:BlockChain):
    if poolId == "DUSD-DFI":
        return len(chain.blocks) * 0.001 + 2
    return None

chain.addWallet(Wallet("oracle",OracleFromLambda(oraclePrice)))
'''
