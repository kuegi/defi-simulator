from typing import List

from enum import Enum


class TxType(Enum):
    PoolSwap = "poolSwap"
    CompositeSwap = "compositeSwap"
    AccountToAccount = "accountToAccount"
    AddLiquidity = "addLiquitity"
    RemoveLiquidity = "removeLiquidity"
    SetOracle= "setOracle"

class Transaction:
    def __init__(self, owner: str, type: TxType):
        self.owner = owner
        self.type = type
        self.confirmedValid= False

    def applyToChain(self, chain):
        raise NotImplementedError

    def isValid(self, chain):
        if self.confirmedValid:
            return True
        self.confirmedValid= self.checkValid(chain)
        return self.confirmedValid

    def checkValid(self,chain):
        raise NotImplementedError

class Token:
    def __init__(self, symbol: str):
        self.symbol = symbol

class Strategy:
    def __init__(self):
        self.owner : Wallet = None

    def createTxs(self,chain) -> List[Transaction]:
        return []

class Wallet:
    def __init__(self, address: str, strategy:Strategy):
        self.address = address
        self.balances = {}
        self.strategy = strategy if strategy is not None else Strategy()
        self.strategy.owner= self

    def __str__(self):
        return self.address+": "+str(self.balances)


class Block:
    def __init__(self, prev, txs: List[Transaction]):
        self.prev = prev
        self.height = prev.height + 1 if prev is not None else 1
        self.txs = txs
