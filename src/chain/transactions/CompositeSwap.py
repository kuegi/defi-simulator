from typing import List

from src.chain.Pool import Pool
from src.chain.blockchain import BlockChain
from src.chain.pojos import Transaction, TxType


class SwapPath:
    def __init__(self,pools:List[Pool],inToken,outToken):
        self.pools= pools
        self.inToken= inToken
        self.outToken= outToken

class CompositeSwap(Transaction):

    def __init__(self, owner: str, to: str, tokenFrom:str, tokenTo:str, pools:List[Pool], amount:float):
        super().__init__(owner=owner, type=TxType.CompositeSwap)
        self.to = to
        self.tokenFrom= tokenFrom
        self.tokenTo = tokenTo
        self.pools= pools
        self.amount = amount

    def calcPriceOnPath(swapPath:SwapPath):
        inToken = swapPath.inToken
        result = 1
        for pool in swapPath.pools:
            AtoB = pool.tokenA.symbol == inToken
            result *= pool.getSwapValueAfterFees(AtoB)
            inToken = pool.tokenB.symbol if AtoB else pool.tokenA.symbol
        return 1/result

    def checkValid(self, chain: BlockChain):
        if self.owner not in chain.wallets or self.to not in chain.wallets\
                or self.tokenFrom not in chain.tokens or self.tokenTo not in chain.tokens:
            return False

        inToken= self.tokenFrom
        for pool in self.pools:
            if inToken != pool.tokenA.symbol and inToken != pool.tokenB.symbol:
                return False
            inToken = pool.tokenB.symbol if pool.tokenA.symbol == inToken else pool.tokenA.symbol

        if inToken != self.tokenTo:
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
        inVolume= self.amount
        inToken= self.tokenFrom
        for pool in self.pools:
            inVolume= pool.swap(inToken,inVolume)
            inToken= pool.tokenB.symbol if inToken == pool.tokenA.symbol else pool.tokenA.symbol

        fromWallet.balances[self.tokenFrom] -= self.amount
        if self.tokenTo not in toWallet.balances:
            toWallet.balances[self.tokenTo]= 0
        toWallet.balances[self.tokenTo] += inVolume