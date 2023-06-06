from typing import List

from src.chain.blockchain import BlockChain
from src.chain.pojos import Strategy, Transaction
from src.chain.transactions.SetOracle import SetOracle


class OracleFromLambda(Strategy):

    def __init__(self, fn):
        super().__init__()
        self.fn= fn

    def createTxs(self,chain) -> List[Transaction]:
        result = []
        for id in chain.oracles.keys():
            price= self.fn(id,chain)
            if price is not None:
                result.append(SetOracle(self.owner.address,id,price))

        return result