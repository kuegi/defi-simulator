
from src.chain.blockchain import BlockChain

class Simulation:

    def __init__(self):
        self.chain= BlockChain()

    def initChain(self):
        raise NotImplementedError()

    def run(self,steps,silent=False):
        for i in range(steps):
            if not silent:
                print(f"\rsimulating {i}/{steps} steps...",end="")
            block = self.chain.blockFromMempool()
            self.chain.addBlock(block)
            for wallet in self.chain.wallets.values():
                txs = wallet.strategy.createTxs(self.chain)
                self.chain.addToMempool(txs)
        if not silent:
           print(f"\rdone simulating {steps} steps")
