import math
import random
from typing import List

from src.chain.pojos import Strategy, Transaction
from src.chain.transactions.CompositeSwap import SwapPath, CompositeSwap
from src.chain.transactions.Swap import Swap

'''
'''
class DUSDBuyStrategy(Strategy):

    def __init__(self, avgVolume,avgFrequency):
        super().__init__()
        self.avgVolume= avgVolume
        self.avgFrequency=avgFrequency

    def calcPriceOnPath(self,pools,firstToken):
        inToken= firstToken
        price= 1
        for pool in pools:
            AtoB = pool.tokenA.symbol == inToken
            price*= pool.getPriceAfterFees(AtoB)
            inToken= pool.tokenB.symbol if AtoB else pool.tokenA.symbol
        return price

    def createTxs(self,chain) -> List[Transaction]:
        result = []
        # random if do buy
        if random.random() < 1/self.avgFrequency:
            # if yes: get best path and swap

            dusddfi= chain.getPool("DUSD","DFI")
            usdtdusd= chain.getPool("USDT","DUSD")
            usdcdusd= chain.getPool("USDC","DUSD")
            usdtdfi= chain.getPool("USDT","DFI")
            usdcdfi= chain.getPool("USDC","DFI")

            paths= [
                SwapPath([usdtdfi,dusddfi],"USDT","DUSD"),
                SwapPath([usdcdfi,dusddfi],"USDC","DUSD"),
                SwapPath([usdcdusd],"USDC","DUSD"),
                SwapPath([usdtdusd],"USDT","DUSD")
            ]

            bestPath= None
            bestPrice= None
            for path in paths:
                price= CompositeSwap.calcPriceOnPath(path)
                if bestPrice is None or price < bestPrice:
                    bestPath= path
                    bestPrice= price

            amount = self.avgVolume * (((random.random() - 0.5) * 0.1) + 1)
            result.append(CompositeSwap(self.owner.address, self.owner.address, bestPath.inToken,
                                        bestPath.outToken,bestPath.pools, amount*bestPrice))

        return result