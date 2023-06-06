import math
from typing import List

from src.chain.pojos import Strategy, Transaction
from src.chain.transactions.CompositeSwap import SwapPath, CompositeSwap
from src.chain.transactions.Swap import Swap

'''
strategy to arb oracle with dex, should be provided with huge funds to simulate arbitrage loops
'''
class ArbPair:
    def __init__(self,oracle,path:SwapPath):
        self.oracle= oracle
        self.path= path

class cexArbStrat(Strategy):

    def __init__(self, minDelta, batchSize, arbs: List[ArbPair]):
        super().__init__()
        self.minDelta= minDelta
        self.batchSize= batchSize
        self.arbs= arbs


    def createTxs(self,chain) -> List[Transaction]:
        result = []
        for arb in self.arbs:
            if arb.oracle not in chain.oracles:
                continue
            buyPrice = CompositeSwap.calcPriceOnPath(arb.path)
            sellPath= SwapPath(list(reversed(arb.path.pools)),arb.path.outToken,arb.path.inToken)
            sellPrice = 1/CompositeSwap.calcPriceOnPath(sellPath)

            oracle= chain.oracles[arb.oracle]

            if 1-buyPrice/oracle > self.minDelta:
                #price below oracle: buy
                result.append(CompositeSwap(self.owner.address,self.owner.address,
                                            arb.path.inToken,arb.path.outToken, arb.path.pools,
                                            self.batchSize))

            if 1-sellPrice/oracle < -self.minDelta:
                #price above oracle: sell
                result.append(CompositeSwap(self.owner.address,self.owner.address,
                                            sellPath.inToken,sellPath.outToken, sellPath.pools,
                                            self.batchSize/sellPrice))

        return result