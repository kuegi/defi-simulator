# A simulator to predict defi markets
from src.chain.Pool import Pool
from src.chain.blockchain import BlockChain
from src.chain.pojos import Token, Wallet

chain = BlockChain()

# init chain
#tokens
chain.addToken(Token("DFI"))
chain.addToken(Token("DUSD"))
# pools
chain.addPool(Pool(chain.tokens["DUSD"],chain.tokens["DFI"]))

# wallets
chain.addWallet(Wallet("wallet1",None))


def doStep():
    block = chain.blockFromMempool()
    chain.addBlock(block)
    for wallet in chain.wallets:
        txs = wallet.strategy.createTxs(chain)
        chain.addToMempool(txs)
