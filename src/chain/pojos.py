from enum import Enum
from typing import List


class Token:
    def __init__(self, symbol: str):
        self.symbol = symbol


class TxType(Enum):
    PoolSwap = "swap"
    AccountToAccount = "accountToAccount"


class Wallet:
    def __init__(self, address: str, strategy):
        self.address = address
        self.balances = {}
        self.strategy = strategy
        if strategy is not None:
            strategy.owner= self


class Transaction:
    def __init__(self, owner: Wallet, type: TxType):
        self.owner = owner
        self.type = type

    def applyToChain(self, chain):
        raise NotImplementedError

    def isValid(self, chain):
        raise NotImplementedError


class Block:
    def __init__(self, prev, txs: List[Transaction]):
        self.prev = prev
        self.height = prev.height + 1 if prev is not None else 1
        self.txs = txs
