from typing import Dict

from src.chain.blockchain import BlockChain
from src.chain.pojos import Transaction, TxType


class AddLiquidity(Transaction):

    def __init__(self, owner: str, balances: Dict[str, float]):
        super().__init__(owner=owner, type=TxType.AddLiquidity)
        self.balances = balances

    def checkValid(self, chain: BlockChain):
        if self.owner not in chain.wallets:
            return False
        if len(self.balances) != 2:
            return False

        keys = list(self.balances.keys())
        a = keys[0]
        b = keys[1]
        pool = chain.getPool(a, b)
        if pool is None:
            return False

        owner = chain.wallets[self.owner]
        for token, amount in self.balances.items():
            if token not in owner.balances or owner.balances[token] < amount:
                return False

        return True

    def applyToChain(self, chain: BlockChain):
        fromWallet = chain.wallets[self.owner]
        keys = list(self.balances.keys())
        a = keys[0]
        b = keys[1]
        pool = chain.getPool(a, b)

        result = pool.addLiquidity(self.balances[pool.tokenA.symbol], self.balances[pool.tokenB.symbol])
        if pool.getSymbol() not in fromWallet.balances:
            fromWallet.balances[pool.getSymbol()] = 0
        fromWallet.balances[pool.getSymbol()] += result

        for token, amount in self.balances.items():
            fromWallet.balances[token] -= amount


class RemoveLiquidity(Transaction):

    def __init__(self, owner: str, pool: str, amount: float):
        super().__init__(owner=owner, type=TxType.RemoveLiquidity)
        self.pool = pool
        self.amount = amount

    def checkValid(self, chain: BlockChain):
        if self.owner not in chain.wallets:
            return False
        if self.pool not in chain.pools:
            return False
        owner = chain.wallets[self.owner]
        if self.pool not in owner.balances or owner.balances[self.pool] < self.amount:
            return False
        return True

    def applyToChain(self, chain: BlockChain):
        fromWallet = chain.wallets[self.owner]
        pool = chain.pools[self.pool]

        result = pool.removeLiquidity(self.amount)
        fromWallet.balances[pool.getSymbol()] -= self.amount

        for token, amount in result.items():
            if token not in fromWallet.balances:
                fromWallet.balances[token] = 0
            fromWallet.balances[token] += amount
