from typing import List, Dict

from .Pool import Pool
from .pojos import Block, Token, Wallet, Transaction


class BlockChain:

    def __init__(self):
        self.mempool: List[Transaction] = []
        self.blocks: List[Block] = []
        self.pools: Dict[str,Pool] = {}
        self.tokens = {}
        self.wallets: Dict[str, Wallet] = {}
        self.oracles = {}
        self.blocks.append(Block(prev=None,txs=[])) #genesis
        self.burn= "BurnAddress"
        self.addWallet(Wallet(self.burn,None))
        self.shouldCheckTxValidity= False

    def addToken(self, token: Token):
        self.tokens[token.symbol] = token

    def addPool(self, pool: Pool):
        self.pools[pool.getSymbol()] = pool
        return pool

    def getPool(self,a:str, b: str):
        if a+"-"+b in self.pools:
            return self.pools[a+"-"+b]
        if b + "-" + a in self.pools:
            return self.pools[b+"-"+a]
        return None

    def addWallet(self, wallet: Wallet):
        self.wallets[wallet.address] = wallet

    def blockFromMempool(self):
        impossibleTxs = []
        txsForBlock = []
        for tx in self.mempool:
            if not self.shouldCheckTxValidity or tx.isValid(self):
                txsForBlock.append(tx)
            else:
                impossibleTxs.append(tx)

        self.mempool = impossibleTxs

        return Block(self.blocks[-1], txsForBlock)

    def addBlock(self, block: Block):
        if (len(self.blocks) == 0 and block.prev is not None) or \
                (len(self.blocks) > 0 and block.prev != self.blocks[-1]):
            print("Error: invalid block prev")
            return

        for tx in block.txs:
            tx.applyToChain(self)

        self.blocks.append(block)

    def addToMempool(self, txs: List[Transaction]):
        # TODO: only allow valid ones?
        self.mempool += txs
