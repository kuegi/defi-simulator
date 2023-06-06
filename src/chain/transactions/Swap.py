from src.chain.blockchain import BlockChain
from src.chain.pojos import Transaction, TxType


class Swap(Transaction):

    def __init__(self, owner: str, to: str, tokenFrom:str, tokenTo:str, amount:float):
        super().__init__(owner=owner, type=TxType.PoolSwap)
        self.to = to
        self.tokenFrom= tokenFrom
        self.tokenTo = tokenTo
        self.amount = amount

    def checkValid(self, chain: BlockChain):
        if self.owner not in chain.wallets or self.to not in chain.wallets\
                or self.tokenFrom not in chain.tokens or self.tokenTo not in chain.tokens:
            return False

        poolId= self.tokenFrom+"-"+self.tokenTo
        if poolId not in chain.pools:
            poolId = self.tokenTo + "-" + self.tokenFrom
        if poolId not in chain.pools:
            return False

        owner = chain.wallets[self.owner]
        if self.tokenFrom not in owner.balances:
            return False
        if owner.balances[self.tokenFrom] < self.amount:
            return False

        return True

    def applyToChain(self, chain: BlockChain):
        fromWallet = chain.wallets[self.owner]
        toWallet = chain.wallets[self.to]
        poolId = self.tokenFrom + "-" + self.tokenTo
        if poolId not in chain.pools:
            poolId = self.tokenTo + "-" + self.tokenFrom
        pool= chain.pools[poolId]
        result= pool.swap(self.tokenFrom,self.amount)
        fromWallet.balances[self.tokenFrom] -= self.amount
        if self.tokenTo not in toWallet.balances:
            toWallet.balances[self.tokenTo]= 0
        toWallet.balances[self.tokenTo] += result