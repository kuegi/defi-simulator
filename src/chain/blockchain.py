from enum import Enum
from typing import List

from .Pool import Pool
from .pojos import Transaction, Block, Token, Wallet


class BlockChain:

    def __init__(self):
        self.mempool: List[Transaction] = []
        self.blocks: List[Block] = []
        self.pools: dict = {}
        self.tokens = {}
        self.wallets = {}
        self.oracles = {}

    def addToken(self,token:Token):
        self.tokens[token.symbol]= token

    def addPool(self,pool:Pool):
        self.pools[pool.getSymbol()]=pool

    def addWallet(self,wallet:Wallet):
        self.wallets[wallet.address]=wallet

    def blockFromMempool(self):
        impossibleTxs = []
        txsForBlock = []
        for tx in self.mempool:
            if tx.isValid(self):
                txsForBlock.append(tx)
            else:
                impossibleTxs.append(tx)

        self.mempool = impossibleTxs

        return Block(self.blocks[-1], txsForBlock)

    def addBlock(self, block: Block):
        if block.prev != self.blocks[-1]:
            print("Error: invalid block prev")
            return

        for tx in block.txs:
            tx.applyToChain(self)

        self.blocks.append(block)

    def addToMempool(self, txs: List[Transaction]):
        # TODO: only allow valid ones?
        self.mempool += txs
