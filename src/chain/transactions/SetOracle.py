from src.chain.blockchain import BlockChain
from src.chain.pojos import Transaction, TxType


class SetOracle(Transaction):

    def __init__(self, owner: str, token: str, price:float):
        super().__init__(owner=owner, type=TxType.SetOracle)
        self.token = token
        self.price= price

    def checkValid(self, chain: BlockChain):
        if self.owner not in chain.wallets:
            return False

        return True

    def applyToChain(self, chain: BlockChain):
        chain.oracles[self.token]=self.price