import math
from typing import List

from src.chain.pojos import Strategy, Transaction
from src.chain.transactions.CompositeSwap import CompositeSwap, SwapPath
from src.chain.transactions.Swap import Swap

'''
strategy to arb oracle with dex, should be provided with huge funds to simulate arbitrage loops
'''
class DUSDLoopArbStrategy(Strategy):

    def __init__(self,batchVolume):
        super().__init__()
        self.batchVolume= batchVolume

    def createTxs(self,chain) -> List[Transaction]:
        result = []
        dusddfi= chain.getPool("DUSD","DFI")
        usdtdusd= chain.getPool("USDT","DUSD")
        usdcdusd= chain.getPool("USDC","DUSD")
        usdtdfi= chain.getPool("USDT","DFI")
        usdcdfi= chain.getPool("USDC","DFI")

        paths= [
            SwapPath([dusddfi,usdtdfi,usdtdusd],"DUSD","DUSD"),
            SwapPath([usdtdusd,usdtdfi,dusddfi],"DUSD","DUSD"),
            SwapPath([dusddfi,usdcdfi,usdcdusd],"DUSD","DUSD"),
            SwapPath([usdcdusd,usdcdfi,dusddfi],"DUSD","DUSD")
        ]
        bestPath= None
        bestPrice= 1
        for path in paths:
            price= CompositeSwap.calcPriceOnPath(path)
            if price < bestPrice:
                bestPath= path
                bestPrice= price

        if bestPath is not None:
            result.append(CompositeSwap(self.owner.address,self.owner.address,"DUSD","DUSD",bestPath.pools,self.batchVolume))

        return result