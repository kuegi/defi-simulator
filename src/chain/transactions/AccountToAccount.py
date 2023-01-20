from typing import Dict

from src.chain.blockchain import BlockChain
from src.chain.pojos import Transaction, TxType, Wallet


class AccountToAccount(Transaction):
    def __init__(self, owner: str, to: str, balances: Dict[str, float]):
        super().__init__(owner=owner, type=TxType.AccountToAccount)
        self.to = to
        self.balances = balances

    def isValid(self, chain: BlockChain):
        if self.owner not in chain.wallets:
            return False

        if self.to not in chain.wallets:
            return False

        owner = chain.wallets[self.owner]
        for token, amount in self.balances.items():
            if token not in owner.balances or owner.balances[token] < amount:
                return False

        return True

    def applyToChain(self, chain: BlockChain):
        fromWallet = chain.wallets[self.owner]
        toWallet = chain.wallets[self.to]

        for token, amount in self.balances.items():
            if token not in fromWallet.balances or fromWallet.balances[token] < amount:
                continue
            if token not in toWallet.balances:
                toWallet.balances[token] = 0
            toWallet.balances[token] += amount
            fromWallet.balances[token] -= amount
