import math
from typing import List

from src.chain.pojos import Strategy, Transaction
from src.chain.transactions.Swap import Swap

'''
strategy for the BBB on defichain
'''
class BBBStrategy(Strategy):

    def __init__(self,dfiPerDay):
        super().__init__()
        self.dfiPerDay= dfiPerDay


    def createTxs(self,chain) -> List[Transaction]:
        result = []
        if len(chain.blocks) % 120 == 0:
            amountPerHour= self.dfiPerDay/24
            result.append(Swap(self.owner.address,chain.burn,"DFI","DUSD",amountPerHour))

        return result