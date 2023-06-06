import math
import random
from typing import List

from src.chain.pojos import Strategy, Transaction
from src.chain.transactions.CompositeSwap import CompositeSwap, SwapPath
from src.chain.transactions.Swap import Swap

'''
'''


class DUSDSellStrategy(Strategy):

    def __init__(self, avgVolume,avgFrequency,toDFIRatio):
        super().__init__()
        self.avgVolume= avgVolume
        self.avgFrequency=avgFrequency
        self.toDFIRatio= toDFIRatio


    def createTxs(self,chain) -> List[Transaction]:
        result = []
        # random if do buy
        if random.random() < 1/self.avgFrequency:
            # if yes: get best path and swap

            amount= self.avgVolume*(((random.random() - 0.5) * 0.1) + 1)

            if random.random() < self.toDFIRatio:
                result.append(Swap(self.owner.address, self.owner.address,"DUSD","DFI", amount))
            else:
                dusddfi= chain.getPool("DUSD","DFI")
                usdtdusd= chain.getPool("USDT","DUSD")
                usdcdusd= chain.getPool("USDC","DUSD")
                usdtdfi= chain.getPool("USDT","DFI")
                usdcdfi= chain.getPool("USDC","DFI")

                paths= [
                    SwapPath([dusddfi,usdtdfi],"DUSD","USDT"),
                    SwapPath([dusddfi,usdcdfi],"DUSD","USDC"),
                    SwapPath([usdcdusd],"DUSD","USDC"),
                    SwapPath([usdtdusd],"DUSD","USDT")
                ]


                bestPath= None
                bestPrice= None
                for path in paths:
                    price= CompositeSwap.calcPriceOnPath(path)
                    if bestPrice is None or price < bestPrice:
                        bestPath= path
                        bestPrice= price
                result.append(CompositeSwap(self.owner.address, self.owner.address, bestPath.inToken,
                                            bestPath.outToken,bestPath.pools, amount))

        return result